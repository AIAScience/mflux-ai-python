=======
History
=======
v0.5.0 (2019-09-01)
-------------------
* add set MLFLOW_TRACKING_TOKEN token in :code:`init`

v0.4.0 (2019-09-01)
-------------------

* Mark :code:`mflux_ai.set_env_vars()` as deprecated. Use :code:`mflux_ai.init()` instead.
* Remove support for Python 3.4
* Add support for secure MinIO connections

v0.3.0 (2019-08-16)
-------------------

* Add a function :code:`init` that will eventually replace :code:`set_env_vars`
* Check if the provided project token is valid.

v0.2.1 (2019-08-16)
-------------------

* Set licence to Apache License 2.0
* Transition from pre-alpha to alpha.

v0.2.0 (2019-08-14)
-------------------

* Add convenience functions for storing and retrieving datasets

v0.1.1 (2019-08-14)
-------------------

* First release on PyPI. Has support for setting environment variables for MLflow based on an MFlux.ai project token.
