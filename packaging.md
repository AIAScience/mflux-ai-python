Steps to upload a new version of the python package

* Check that all unit tests are OK
* Check that the python package version to be released is compatible with the currently deployed API
* Bump the version number in `mflux_ai/__init__.py` in accordance with the [semantic versioning specification](https://semver.org/)
* Update `HISTORY.rst`
* Commit and push the change with a commit message like this: "Release vx.y.z" (replace x.y.z with the package version)
* `python setup.py sdist bdist_wheel`
* `python -m twine upload dist/*`
* Add and push a git tag to the release commit
