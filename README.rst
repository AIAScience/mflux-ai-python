========
mflux-ai
========


.. image:: https://img.shields.io/pypi/v/mflux_ai.svg
        :target: https://pypi.python.org/pypi/mflux_ai

.. image:: https://img.shields.io/travis/AIAScience/mflux_ai.svg
        :target: https://travis-ci.org/AIAScience/mflux_ai

.. image:: https://readthedocs.org/projects/mflux-ai/badge/?version=latest
        :target: https://mflux-ai.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Official the mflux-ai python library.



* Free software: BSD license
* Documentation: https://mflux-ai.readthedocs.io.

Features
--------
- acquire and set environment variables required by mflux-server
- cache the environment variables


Quickstart
----------
Install mflux-ai

    pip install mflux-ai

Import mflux_ai

    Import  mflux-ai

    mflux_ai.set_env_vars(token="9s9kQ0D86wWKUHdPMj0HHA", server_host"http://localhost:8000")


More example
------------
You can also use MfluxClient from mflux_ai

    from mflux_ai import MfluxClient

    # create instance of mflux client

    client = MfluxClient(token="9s9kQ0D86wWKUHdPMj0HHA", server_host"http://localhost:8000")

    # set environment variables required for the project

    client.set_env_vars()

    # save the environment variables to file

    client.save_cache_to_file()

    # set the  environment variables from the cache file

    client.set_env_vars_from_cache_file()



