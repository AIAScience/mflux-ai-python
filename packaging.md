Upload the python package to https://test.pypi.org/

* `python setup.py sdist bdist_wheel`
* `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
