#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import codecs
import os
import re

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["joblib<1", "minio>=4,<5", "mlflow>=1.2.0,<2", "requests"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest", "responses"]

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    author="AIA Science AS",
    author_email="mflux.ai@aiascience.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Version Control",
    ],
    description="The Python client for MFlux.ai",
    install_requires=requirements,
    license="Apache License 2.0",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="mflux_ai mlflow ml tracking ai workflow machine learning object storage dataset versioning",
    name="mflux-ai",
    packages=find_packages(include=["mflux_ai"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    python_requires=">=3.5, <4",
    url="https://github.com/AIAScience/mflux-ai-python",
    version=find_version("mflux_ai", "__init__.py"),
    zip_safe=False,
)
