#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mflux_ai` package."""
import os

import responses
from mflux_ai.mflux_ai import MfluxClient


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
            method="GET",
            url="http://mflux-server.com/api/env_vars/",
            json=content,
            status=200,
        )
    )

    mflux_client = MfluxClient(
        token="thisshouldbevalidtoken", server_host="http://mflux-server.com"
    )

    assert mflux_client.get_env_vars() == content
    assert mflux_client.set_env_vars() == True
    assert os.environ.get("MLFLOW_TRACKING_URI") == content["mlflow_server"]
    assert os.environ.get("MLFLOW_S3_ENDPOINT_URL") == content["minio_server"]
    assert os.environ.get("AWS_SECRET_ACCESS_KEY") == content["minio_secret_key"]
    assert os.environ.get("AWS_ACCESS_KEY_ID") == content["minio_access_key"]
