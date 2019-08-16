# -*- coding: utf-8 -*-
from .mflux_ai import *

"""Top-level package for mflux-ai."""

__author__ = """AIA Science AS"""
__email__ = "mflux.ai@aiascience.com"
__version__ = "0.3.0"


def set_env_vars(token):
    # TODO: Uncomment the following deprecation warning later
    # print('Warning: mflux_ai.set_env_vars is deprecated. Please use mflux.init instead.')
    return init(token)
