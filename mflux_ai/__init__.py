# -*- coding: utf-8 -*-
from .mflux_ai import *
"""Top-level package for mflux-ai."""

__author__ = """AIA Science AS"""
__email__ = "mflux.ai@aiascience.com"
__version__ = "0.1.0"


def set_env_vars(token):
    try:
        MfluxClient(token=token).set_env_vars()
        return True
    except Exception as e:
        print("couldn't connect to mflux server :", e)

