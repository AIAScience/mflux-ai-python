# -*- coding: utf-8 -*-
import warnings

from .mflux_ai import (
    init,
    get_minio_client,
    ensure_bucket_exists,
    put_dataset,
    get_dataset,
)

"""Top-level package for mflux-ai."""

__author__ = """AIA Science AS"""
__email__ = "mflux.ai@aiascience.com"
__version__ = "0.5.2"


def set_env_vars(token):
    warnings.warn(
        "mflux_ai.set_env_vars() is deprecated. Please use mflux.init() instead.",
        DeprecationWarning,
    )
    return init(token)
