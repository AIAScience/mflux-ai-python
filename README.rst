========
mflux-ai
========


.. image:: https://img.shields.io/pypi/v/mflux_ai.svg
        :target: https://pypi.python.org/pypi/mflux_ai

.. image:: https://img.shields.io/travis/AIAScience/mflux-ai-python.svg?branch=master
        :target: https://travis-ci.org/AIAScience/mflux-ai-python

Open source code for the :code:`mflux-ai` python library.

Features
--------
- Fetch connection strings and tell MLflow how to connect with MFlux.ai
- Download and upload objects/datasets from/to the MFlux.ai cloud service

Quickstart
----------
Installation

    pip install mflux-ai

Basic usage

.. code:: python

    import mflux_ai

    mflux_ai.init("INSERT_YOUR_PROJECT_TOKEN_HERE")

    # MLflow now knows how to connect with your project server, hosted on MFlux.ai

Store and retrieve datasets

.. code:: python

    my_dataset = np.zeros(shape=(10000, 100), dtype=np.float32)
    dataset_filename = "my-dataset.pkl"

    mflux_ai.put_dataset(my_dataset, dataset_filename)

    my_loaded_dataset = mflux_ai.get_dataset(dataset_filename)

    assert_array_equal(my_dataset, my_loaded_dataset)
