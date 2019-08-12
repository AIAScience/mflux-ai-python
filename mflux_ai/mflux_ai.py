# -*- coding: utf-8 -*-

"""Main module."""
import json
import os

import requests

SERVER_HOST = "http://localhost:8000"


class MfluxClient(object):
    def __init__(self, token: str, server_ip=SERVER_HOST) -> None:
        server_ip = server_ip + "/env_vars"
        token = token  # yourAccessTokenHere#
        headers = {
            "Content-Type": "application/json",
            "Authorization": "api-key {}".format(token),
        }

        self.cache_file_name = "aia-mflux-{token}-{project}.json".format(
            token=token, project="aia-001"
        )
        self.env_vars = requests.get(server_ip, headers=headers)
        self.variables = {}
        if self.env_vars.status_code == 200:
            self.variables = json.loads(self.env_vars.content)
            with open(self.cache_file_name, "w") as cache_file:
                json.dump(self.variables, cache_file)

    def set_env_vars(self,):
        if self.variables:
            if (
                self.variables["minio_secret_key"]
                and self.variables["minio_access_key"]
                and self.variables["minio_server"]
                and self.variables["mlflow_server"]
            ):
                os.environ["MLFLOW_TRACKING_URI"] = self.variables["mlflow_server"]
                os.environ["MLFLOW_S3_ENDPOINT_URL"] = self.variables["minio_server"]
                os.environ["AWS_ACCESS_KEY_ID"] = self.variables["minio_access_key"]
                os.environ["AWS_SECRET_ACCESS_KEY"] = self.variables["minio_secret_key"]
                return True
        else:
            return False

    def get_env_vars(self):
        if self.set_env_vars():
            variables = json.loads(self.env_vars.content)
            return variables
        else:
            return self.variables

    def get_env_vars_from_cache_file(self):
        if self.set_env_vars():
            with open(self.cache_file_name, "r") as cache_file:
                env_from_file = json.load(cache_file)
                return env_from_file
        else:
            return self.variables
