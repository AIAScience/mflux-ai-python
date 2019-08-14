# -*- coding: utf-8 -*-

"""Main module."""
import json
import os

import joblib
import requests
import tempfile

from minio import Minio
from minio.error import BucketAlreadyOwnedByYou, BucketAlreadyExists, ResponseError

SERVER_HOST = "https://www.mflux.ai"
_minio_client = None


class MfluxClient(object):
    def __init__(self, token, server_host=SERVER_HOST):
        server_ip = server_host + "/api/env_vars/"
        token = token  # yourAccessTokenHere#
        headers = {
            "Content-Type": "application/json",
            "Authorization": "api-key {}".format(token),
        }
        self.variables = dict()
        self.cache_file_name = "aia-mflux-{token}.json".format(token=token)
        try:
            self.env_vars = requests.get(server_ip, headers=headers)
        except requests.exceptions.RequestException as e:
            print("Couldnt connect to mflux-server :", e)
        if self.env_vars.status_code == 200:
            self.variables = json.loads(self.env_vars.content)

    def set_env_vars(self,):
        if self.variables:
            if not (
                self.variables["minio_secret_key"]
                and self.variables["minio_access_key"]
                and self.variables["minio_server"]
                and self.variables["mlflow_server"]
            ):
                return False
            os.environ["MLFLOW_TRACKING_URI"] = self.variables["mlflow_server"]
            os.environ["MLFLOW_S3_ENDPOINT_URL"] = self.variables["minio_server"]
            os.environ["AWS_ACCESS_KEY_ID"] = self.variables["minio_access_key"]
            os.environ["AWS_SECRET_ACCESS_KEY"] = self.variables["minio_secret_key"]

            return True

    def get_env_vars(self):
        if self.set_env_vars():
            variables = json.loads(self.env_vars.content)
            return variables
        else:
            return self.variables

    def get_env_vars_from_cache_file(self):
        try:
            with open(self.cache_file_name, "r") as cache_file:
                env_from_file = json.load(cache_file)
                return env_from_file
        except FileNotFoundError:
            print("Could not open file:", self.cache_file_name)

    def set_env_vars_from_cache_file(self):
        try:
            with open(self.cache_file_name, "r") as cache_file:
                self.variables = json.load(cache_file)
                self.set_env_vars()

        except FileNotFoundError:
            print("Could not open file:", self.cache_file_name)

    def save_cache_to_file(self):
        if self.variables:
            try:
                with open(self.cache_file_name, "w") as cache_file:
                    json.dump(self.variables, cache_file)
            except IOError:
                print("Could not create file:", self.cache_file_name)


def get_minio_client():
    """Return a Minio instance. If one has been created earlier, return the same instance."""
    global _minio_client

    assert os.environ.get("MLFLOW_S3_ENDPOINT_URL", None) is not None
    assert os.environ.get("AWS_ACCESS_KEY_ID", None) is not None
    assert os.environ.get("AWS_SECRET_ACCESS_KEY", None) is not None
    if not _minio_client:
        _minio_client = Minio(
            os.environ["MLFLOW_S3_ENDPOINT_URL"]
            .replace("http://", "")
            .replace(":9000/", ":9000"),
            access_key=os.environ["AWS_ACCESS_KEY_ID"],
            secret_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            secure=False,
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
