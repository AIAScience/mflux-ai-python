#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mflux_ai` package."""
import os

import responses

import mflux_ai
from mflux_ai import MfluxClient, SERVER_HOST


@responses.activate
def test_mflux_ai():
    content = {
        "minio_secret_key": "minio_secret",
        "minio_access_key": "minio_access",
        "minio_server": "http://192.198.0.1:9000",
        "mlflow_server": "http://192.198.0.1:5000",
    }

    responses.add(
        responses.Response(
            method="GET", url=SERVER_HOST + "/env_vars/", json=content, status=200
        )
    )

    mflux_client = MfluxClient(token="thisshouldbevalidtoken")

    assert mflux_client.get_env_vars() == content
    assert mflux_client.set_env_vars() == True
    assert os.environ.get("MLFLOW_TRACKING_URI") == content["mlflow_server"]
    assert os.environ.get("MLFLOW_S3_ENDPOINT_URL") == content["minio_server"]
    assert os.environ.get("AWS_SECRET_ACCESS_KEY") == content["minio_secret_key"]
    assert os.environ.get("AWS_ACCESS_KEY_ID") == content["minio_access_key"]
    assert mflux_ai.set_env_vars(token="thisshouldbevalidtoken") == True
