=======
History
=======

v0.5.3 (2019-09-23)
-------------------

* Improve the performance and the support for special characters in object names in :code:`mflux_ai.get_dataset` by unpickling in memory instead of using a temporary file on disk.
* Don't expose non-public variables and imports on the top-level package

v0.5.2 (2019-09-20)
-------------------

* Improve the performance of :code:`mflux_ai.put_dataset` by pickling in memory instead of using a temporary file on disk.

v0.5.1 (2019-09-12)
-------------------

* Add support for MLflow authentication
* Improve the performance of :code:`mflux_ai.put_dataset`
* Correctly reset the MinIO client when :code:`init` completes successfully
* Specify the desired API version and let the user know if an upgrade is needed

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
