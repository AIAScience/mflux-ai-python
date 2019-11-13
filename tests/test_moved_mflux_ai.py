#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mflux_ai.mflux.ai`, which is now deprecated."""
import os
import warnings

import responses

from mflux_ai import mflux_ai
from mflux_ai import core as mflux_ai_core


@responses.activate
def test_mflux_ai_init():
    """Test that the init function still works, although it has been moved. It should raise a
     DeprecationWarning."""
    content = {
        "minio_secret_key": "minio_secret",
        "minio_access_key": "minio_access",
        "minio_server": "http://192.198.0.1:9000",
        "mlflow_server": "http://192.198.0.1:5000",
    }

    responses.add(
        responses.Response(
            method="GET", url=mflux_ai.SERVER_HOST + "/api/env_vars/", json=content, status=200
        )
    )

    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        mflux_ai.init("thisshouldbevalidtoken")
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "has been moved" in str(w[-1].message)

    assert os.environ.get("MLFLOW_TRACKING_URI") == content["mlflow_server"]
    assert os.environ.get("MLFLOW_S3_ENDPOINT_URL") == content["minio_server"]
    assert os.environ.get("AWS_SECRET_ACCESS_KEY") == content["minio_secret_key"]
    assert os.environ.get("AWS_ACCESS_KEY_ID") == content["minio_access_key"]
    assert os.environ.get("MLFLOW_TRACKING_TOKEN") == "thisshouldbevalidtoken"


@responses.activate
def test_change_deprecated_server_host_variable():
    """Test that the deprecated SERVER_HOST variable still works, although it has been moved.
    Changing this variable should raise a DeprecationWarning."""
    mflux_ai.SERVER_HOST = "https://test.mflux.ai"
    content = {
        "minio_secret_key": "minio_secret",
        "minio_access_key": "minio_access",
        "minio_server": "http://192.198.0.1:9000",
        "mlflow_server": "http://192.198.0.1:5000",
    }

    responses.add(
        responses.Response(
            method="GET", url=mflux_ai.SERVER_HOST + "/api/env_vars/", json=content, status=200
        )
    )

    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        mflux_ai_core.init("thisshouldbevalidtoken")
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "The internal SERVER_HOST variable has been moved" in str(w[-1].message)

    assert os.environ.get("MLFLOW_TRACKING_URI") == content["mlflow_server"]
    assert os.environ.get("MLFLOW_S3_ENDPOINT_URL") == content["minio_server"]
    assert os.environ.get("AWS_SECRET_ACCESS_KEY") == content["minio_secret_key"]
    assert os.environ.get("AWS_ACCESS_KEY_ID") == content["minio_access_key"]
    assert os.environ.get("MLFLOW_TRACKING_TOKEN") == "thisshouldbevalidtoken"
