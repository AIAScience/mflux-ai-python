# -*- coding: utf-8 -*-

import os
import tempfile

import joblib
import requests
from minio import Minio
from minio.error import BucketAlreadyOwnedByYou, BucketAlreadyExists, ResponseError

SERVER_HOST = "https://www.mflux.ai"
_minio_client = None


def init(project_token):
    """
    Fetch connection strings and set them as environment variables that MLflow understands and
    uses when it connects to your MFlux.ai server.

    :param project_token: A secret string that is specific to an MFlux.ai project that you have
        access to.
    """
    global _minio_client
    if "your_" in project_token.lower():
        print(
            "Warning: {} looks like an invalid project token. Go to"
            " {}/dashboard/ to obtain your project token.".format(
                project_token, SERVER_HOST
            )
        )

    headers = {
        "Accept": "application/vnd.aiascience.mflux+json; version=0.4",
        "Authorization": "api-key {}".format(project_token),
    }
    url = SERVER_HOST + "/api/env_vars/"
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
        print(
            "Error: Could not connect to the MFlux.ai server ({}). If this issue persists,"
            " please contact MFlux.ai's support.".format(SERVER_HOST)
        )
        raise

    if response.status_code != 200:
        if response.status_code == 406 and "Invalid version" in str(response.content):
            # We import __version__ here to avoid circular imports
            from . import __version__

            raise Exception(
                "Error: Bad status code {}. This may indicate your mflux-ai python package"
                " needs to be upgraded to a newer version. Currently, mflux-ai=={} is"
                " installed. Go to https://pypi.org/project/mflux-ai/ to see what the latest"
                " version of mflux-ai is.".format(
                    response.status_code, __version__
                )
            )
        elif response.status_code == 204:
            raise Exception(
                "Error: Bad status code {}. This may indicate that your project token is"
                " invalid.".format(response.status_code)
            )
        else:
            raise Exception(
                "Error: Bad status code {}. If this issue persists,"
                " please contact MFlux.ai's support.".format(response.status_code)
            )

    data = response.json()
    if not data.get("mlflow_server", None):
        print("Error: Could not fetch mlflow_server connection string")
    if not data.get("minio_server", None):
        print("Error: Could not fetch minio_server connection string")
    if not data.get("minio_access_key", None):
        print("Error: Could not fetch minio_access_key connection string")
    if not data.get("minio_secret_key", None):
        print("Error: Could not fetch minio_secret_key connection string")

    _minio_client = None
    os.environ["MLFLOW_TRACKING_URI"] = data.get("mlflow_server", None)
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = data.get("minio_server", None)
    os.environ["AWS_ACCESS_KEY_ID"] = data.get("minio_access_key", None)
    os.environ["AWS_SECRET_ACCESS_KEY"] = data.get("minio_secret_key", None)
    os.environ["MLFLOW_TRACKING_TOKEN"] = project_token


def get_minio_client():
    """Return a Minio instance. If one has been created earlier, return the same instance."""
    global _minio_client

    assert os.environ.get("MLFLOW_S3_ENDPOINT_URL", None) is not None
    assert os.environ.get("AWS_ACCESS_KEY_ID", None) is not None
    assert os.environ.get("AWS_SECRET_ACCESS_KEY", None) is not None
    if not _minio_client:
        is_secure = "https://" in os.environ["MLFLOW_S3_ENDPOINT_URL"]
        endpoint = (
            os.environ["MLFLOW_S3_ENDPOINT_URL"]
            .replace("http://", "")
            .replace("https://", "")
            .replace(":9000/", ":9000")  # TODO: Remove this replace
        )
        _minio_client = Minio(
            endpoint,
            access_key=os.environ["AWS_ACCESS_KEY_ID"],
            secret_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            secure=is_secure,
        )

    return _minio_client


def ensure_bucket_exists(bucket_name):
    """Create a bucket with the given bucket_name if it doesn't already exist."""
    minio_client = get_minio_client()

    try:
        minio_client.make_bucket(bucket_name)
    except BucketAlreadyOwnedByYou as err:
        pass
    except BucketAlreadyExists as err:
        pass
    except ResponseError as err:
        raise


def put_dataset(value, object_name, bucket_name="datasets"):
    """
    Store an object/dataset in the MFlux.ai cloud. It gets pickled by joblib.dump.

    :param value: The object/dataset to store. It should be picklable.
    :param object_name: The name of the dataset
    :param bucket_name: (Optional, defaults to "datasets") Name of the bucket to store the
        object/dataset in. Think of it as a folder. This name must not contain underscores. For
        more info on bucket name restrictions, see
        https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html
        If the bucket does not already exist, it will be created.
    :return:
    """
    minio_client = get_minio_client()

    ensure_bucket_exists(bucket_name)

    tmp_file_path = os.path.join(tempfile.gettempdir(), object_name)
    joblib.dump(value, tmp_file_path, compress=True)

    try:
        minio_client.fput_object(
            bucket_name, object_name=object_name, file_path=tmp_file_path
        )
    except ResponseError as err:
        print(err)


def get_dataset(object_name, bucket_name="datasets"):
    """
    Retrieve the object/dataset with the given object_name from the MFlux.ai cloud. The object
    gets unpickled by joblib.load.
    """
    minio_client = get_minio_client()

    downloaded_file_path = os.path.join(tempfile.gettempdir(), object_name)
    try:
        data = minio_client.get_object(bucket_name, object_name)
        with open(downloaded_file_path, "wb") as file_data:
            for d in data.stream(32 * 1024):
                file_data.write(d)
    except ResponseError as err:
        raise

    return joblib.load(downloaded_file_path)
