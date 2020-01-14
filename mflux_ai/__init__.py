# -*- coding: utf-8 -*-
import warnings

import mflux_ai.mflux_ai as mflux_ai
from .core import (
    init,
    get_minio_client,
    ensure_bucket_exists,
    put_dataset,
    get_dataset,
    get_best_run,
)

"""Top-level package for mflux-ai."""

__author__ = """AIA Science AS"""
__email__ = "mflux.ai@aiascience.com"
__version__ = "0.6.0"


def set_env_vars(token):
    warnings.warn(
        "mflux_ai.set_env_vars() is deprecated. Please use mflux_ai.init() instead.",
        DeprecationWarning,
    )
    return init(token)
