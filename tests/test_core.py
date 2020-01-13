#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `mflux_ai` package."""
import os
import warnings

import responses


import mlflow
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

    env_content = {
        "minio_secret_key": "minio_secret",
        "minio_access_key": "minio_access",
        "minio_server": "http://192.198.0.1:9000",
        "mlflow_server": "http://192.198.0.1:5000",
    }

    responses.add(
        responses.Response(
            method="GET", url=SERVER_HOST + "/api/env_vars/", json=env_content, status=200
        )
    )

    mflux_ai.init("thisshouldbevalidtoken")

    headers = {
        "User-Agent": "mlflow-python-client/1.0.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Authorization": "Bearer thisshouldbevalidtoken",
    }

    content = {
        "run": {
            "info": {
                "run_uuid": "123",
                "experiment_id": "2",
                "user_id": "Iver",
                "status": "FINISHED",
                "start_time": "1577979142226",
                "end_time": "1577979155221",
                "artifact_uri": "s3://mlflow/2/123/artifacts",
                "lifecycle_stage": "active",
                "run_id": "123",
            },
            "data": {
                "metrics": [
                    {
                        "key": "error",
                        "value": 1.06968755342329e-05,
                        "timestamp": "1577979154751",
                        "step": "49",
                    }
                ],
                "params": [{"key": "optimizer_name", "value": "FastGANoisyDiscreteOnePlusOne"}],
                "tags": [
                    {"key": "mlflow.user", "value": "Iver"},
                    {
                        "key": "mlflow.source.name",
                        "value": "C:/Users/Iver/Code/mflux-quickstart/nevergrad_example.py",
                    },
                    {"key": "mlflow.source.type", "value": "LOCAL"},
                ],
            },
        }
    }

    url = (
        env_content["mlflow_server"]
        + "/api/2.0/preview/mlflow/runs/get?run_uuid=123&run_id=123"
    )

    responses.add(
        responses.Response(method="GET", url=url, json=content, status=200, headers=headers),
        match_querystring=True,
    )

    headers = {
        "Content-Type": "application/vnd.aiascience.mflux+json; version=0.4",
        "Authorization": "api-key {}".format("thisshouldbevalidtoken"),
    }
    content = {"run_uuid": "123"}

    url = SERVER_HOST + "/api/best_run_by_model_group/best_run/?model_group_name={}".format(
        "model_name"
    )

    responses.add(
        responses.Response(method="GET", url=url, json=content, status=200, headers=headers)
    )

    best_run = mflux_ai.core.get_best_run("model_name")
    assert isinstance(best_run, mlflow.entities.run.Run)
    assert best_run.info.run_uuid == content["run_uuid"]
