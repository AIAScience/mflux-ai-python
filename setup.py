#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["joblib<1", "minio>=4,<5", "requests"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest", "responses"]

setup(
    author="AIA Science AS",
    author_email="mflux.ai@aiascience.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="The Python client for MFlux.ai",
    install_requires=requirements,
    license="Apache License 2.0",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="mflux_ai mlflow ml tracking ai workflow object storage dataset versioning",
    name="mflux-ai",
    packages=find_packages(include=["mflux_ai"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    python_requires=">=3.5, <4",
    url="https://github.com/AIAScience/mflux-ai-python",
    version="0.4.0",
    zip_safe=False,
)
