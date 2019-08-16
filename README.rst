========
mflux-ai
========


.. image:: https://img.shields.io/pypi/v/mflux_ai.svg
        :target: https://pypi.python.org/pypi/mflux_ai

.. image:: https://img.shields.io/travis/AIAScience/mflux-ai-python.svg?branch=master
        :target: https://travis-ci.org/AIAScience/mflux-ai-python

Open source code for the mflux-ai python library.

Features
--------
- Acquire and set environment variables required by mflux-server

Quickstart
----------
Installation

    pip install mflux-ai

Usage

.. code:: python

    import mflux_ai

    mflux_ai.set_env_vars(token="insert_your_token_here")

Storing and retrieving datasets

.. code:: python

    my_dataset = np.zeros(shape=(10000, 100), dtype=np.float32)
    dataset_filename = "my-dataset.pkl"

    mflux_ai.put_dataset(my_dataset, dataset_filename)

    my_loaded_dataset = mflux_ai.get_dataset(dataset_filename)

    assert_array_equal(my_dataset, my_loaded_dataset)
