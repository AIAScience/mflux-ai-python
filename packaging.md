Steps to upload a new version of the python package

* Bump the version number in `setup.py` and `mflux_ai/__init__.py`
* `python setup.py sdist bdist_wheel`
* `python -m twine upload dist/*`
