# -*- coding: utf-8 -*-

import io
import os
import warnings

import joblib
import requests
from minio import Minio
from minio.error import (
    BucketAlreadyOwnedByYou,
    BucketAlreadyExists,
    NoSuchBucket,
    ResponseError,
)

SERVER_HOST = "https://www.mflux.ai"
#mflux_ai.core.SERVER_HOST = "http://localhost:8000"


_minio_client = None


def init(project_token):
    """
    Fetch connection strings and set them as environment variables that MLflow understands and
    uses when it connects to your MFlux.ai server.

    :param project_token: A secret string that is specific to an MFlux.ai project that you have
        access to.
    """
    global _minio_client
    global SERVER_HOST
    if "your_" in project_token.lower():
        print(
            'Warning: "{}" looks like an invalid project token. Go to'
            " {}/dashboard/ to obtain your project token.".format(project_token, SERVER_HOST)
        )

    from mflux_ai.mflux_ai import SERVER_HOST as DEPRECATED_SERVER_HOST_VARIABLE

    if DEPRECATED_SERVER_HOST_VARIABLE != "https://www.mflux.ai":
        warnings.warn(
            "The internal SERVER_HOST variable has been moved. If you are doing\n"
            "from mflux_ai import mflux_ai\n"
            "mflux_ai.SERVER_HOST = ...\n"
            "or\n"
            "import mflux_ai\n"
            "mflux_ai.mflux_ai.SERVER_HOST = ...\n"
            "then you should instead do this:\n"
            "import mflux_ai\n"
            "mflux_ai.core.SERVER_HOST = ...",
            DeprecationWarning,
        )
        # Note: This will be changed from warning to error in a future version
        SERVER_HOST = DEPRECATED_SERVER_HOST_VARIABLE

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
                " version of mflux-ai is.".format(response.status_code, __version__)
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

    in_memory_file = io.BytesIO()
    joblib.dump(value, in_memory_file, compress=True)
    num_bytes = in_memory_file.getbuffer().nbytes

    # Prepare for the read() call on the in-memory file object
    in_memory_file.seek(0)

    for _ in range(2):
        try:
            minio_client.put_object(bucket_name, object_name, in_memory_file, num_bytes)
            break  # Success! Now exit the loop
        except ResponseError as err:
            print(err)
            break  # Failure, no retry
        except NoSuchBucket:
            ensure_bucket_exists(bucket_name)
            continue  # Try the object upload again now that the bucket has been created


def get_dataset(object_name, bucket_name="datasets"):
    """
    Retrieve the object/dataset with the given object_name from the MFlux.ai cloud. The object
    gets unpickled by joblib.load.
    """
    minio_client = get_minio_client()

    in_memory_file = io.BytesIO()
    try:
        data = minio_client.get_object(bucket_name, object_name)
        for d in data.stream(32 * 1024):
            in_memory_file.write(d)
    except ResponseError as err:
        raise

    # Prepare for the read() call on the in-memory file object
    in_memory_file.seek(0)

    return joblib.load(in_memory_file)


def get_best_run(model_group_name):
    """
    Fetch the run id for the best run in a model group

    :param model_group_name:
    """

    project_token = os.environ["MLFLOW_TRACKING_TOKEN"]


    headers = {
        "Content-Type": "application/vnd.aiascience.mflux+json; version=0.4",
        "Authorization": "api-key {}".format(project_token),
    }
    url = SERVER_HOST + "/api/best_run_by_model_group/best_run/?model_group_name={}".format(model_group_name)
    try:
        response = requests.get(url, headers=headers)
        print(response)
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
                " version of mflux-ai is.".format(response.status_code, __version__)
            )
        elif response.status_code == 204:
            raise Exception(
                "Error: Bad status code {}. This may indicate that your project token is"
                " invalid.".format(response.status_code)
            )
        elif response.status_code == 404:
            raise Exception(
                "Error: Bad status code {}. This may indicate that the model group does"
                " not exists.".format(response.status_code)
            )
        else:
            raise Exception(
                "Error: Bad status code {}. If this issue persists,"
                " please contact MFlux.ai's support.".format(response.status_code)
            )

    data = response.json()
    return data



