Steps to upload a new version of the python package

* Check that all unit tests are OK
* Bump the version number in `setup.py` and `mflux_ai/__init__.py`
* Update `HISTORY.rst`
* `python setup.py sdist bdist_wheel`
* `python -m twine upload dist/*`
* Add git tag
