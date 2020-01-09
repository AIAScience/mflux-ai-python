#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `mflux_ai` package."""
import os
import warnings

import responses

import mflux_ai
from mflux_ai.core import SERVER_HOST


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
    assert os.environ.get("MLFLOW_TRACKING_TOKEN") == "thisshouldbevalidtoken"


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

    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        mflux_ai.set_env_vars("thisshouldbevalidtoken")
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message)

    assert os.environ.get("MLFLOW_TRACKING_URI") == content["mlflow_server"]
    assert os.environ.get("MLFLOW_S3_ENDPOINT_URL") == content["minio_server"]
    assert os.environ.get("AWS_SECRET_ACCESS_KEY") == content["minio_secret_key"]
    assert os.environ.get("AWS_ACCESS_KEY_ID") == content["minio_access_key"]
    assert os.environ.get("MLFLOW_TRACKING_TOKEN") == "thisshouldbevalidtoken"


@responses.activate
def test_get_best_run():

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

    content = {
    "run_uuid" : "123"
    }

    headers = {
        "Content-Type": "application/vnd.aiascience.mflux+json; version=0.4",
        "Authorization": "api-key {}".format("thisshouldbevalidtoken"),
    }

    url = SERVER_HOST + "/api/best_run_by_model_group/best_run/?model_group_name={}".format("model_name")

    responses.add(
        responses.Response(
            method="GET", url=url, json=content, status=200, headers= headers
        )
    )

    best_run = mflux_ai.core.get_best_run("model_name")
    assert best_run['run_uuid'] == content['run_uuid']

