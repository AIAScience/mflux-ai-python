#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `mflux_ai` package."""
import os

import responses

import mflux_ai
from mflux_ai import SERVER_HOST


@responses.activate
def test_mflux_ai_init():
    """Test the init function."""
    content = {
        "minio_secret_key": "minio_secret",
        "minio_access_key": "minio_access",
        "minio_server": "http://192.198.0.1:9000",
        "mlflow_server": "http://192.198.0.1:5000",
    }

    responses.add(
        responses.Response(
            method="GET", url=SERVER_HOST + "/api/env_vars/", json=content, status=200
        )
    )

    mflux_ai.init("thisshouldbevalidtoken")
    assert os.environ.get("MLFLOW_TRACKING_URI") == content["mlflow_server"]
    assert os.environ.get("MLFLOW_S3_ENDPOINT_URL") == content["minio_server"]
    assert os.environ.get("AWS_SECRET_ACCESS_KEY") == content["minio_secret_key"]
    assert os.environ.get("AWS_ACCESS_KEY_ID") == content["minio_access_key"]
    assert os.environ.get("MFLUX_AI_PROJECT_TOKEN") == "thisshouldbevalidtoken"


@responses.activate
def test_mflux_ai_deprecated_set_env_vars():
    """Test the deprecated set_env_vars function."""
    content = {
        "minio_secret_key": "minio_secret",
        "minio_access_key": "minio_access",
        "minio_server": "http://192.198.0.1:9000",
        "mlflow_server": "http://192.198.0.1:5000",
    }

    responses.add(
        responses.Response(
            method="GET", url=SERVER_HOST + "/api/env_vars/", json=content, status=200
        )
    )

    mflux_ai.set_env_vars("thisshouldbevalidtoken")
    assert os.environ.get("MLFLOW_TRACKING_URI") == content["mlflow_server"]
    assert os.environ.get("MLFLOW_S3_ENDPOINT_URL") == content["minio_server"]
    assert os.environ.get("AWS_SECRET_ACCESS_KEY") == content["minio_secret_key"]
    assert os.environ.get("AWS_ACCESS_KEY_ID") == content["minio_access_key"]
    assert os.environ.get("MFLUX_AI_PROJECT_TOKEN") == "thisshouldbevalidtoken"
