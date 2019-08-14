# -*- coding: utf-8 -*-

"""Main module."""
import json
import os

import requests

SERVER_HOST = "https://www.mflux.ai"


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

    def save_cache_to_file(self):
        if self.variables:
            try:
                with open(self.cache_file_name, "w") as cache_file:
                    json.dump(self.variables, cache_file)
            except IOError:
                print("Could not create file:", self.cache_file_name)
