#!/usr/bin/env python

import sys

from setuptools import setup

try:
    from typing import List
except Exception:
    pass

# Define __version__.  This is equivalent to execfile but works in Python 3.
with open("groupy/version.py", "r") as version:
    code = compile(version.read(), "groupy/version.py", "exec")
    exec(code)

# Installation requirements.
with open("requirements.txt") as requirements:
    requires = requirements.read().splitlines()

# Test suite requirements.
with open("requirements-dev2.txt") as requirements:
    test_requires = requirements.read().splitlines()

# Add pytest-runner to setup_requires if running setup with the test argument.
setup_requires = []  # type: List[str]
if "test" in sys.argv:
    setup_requires += ["pytest-runner"]

kwargs = {
    "name": "groupy",
    "version": __version__,  # type: ignore  # noqa: F821
    "packages": ["groupy"],
    "description": "Python client library for Grouper",
    "long_description": open("README.rst").read(),
    "author": "Gary M. Josack, Mark Smith, Herbert Ho, Luke Faraone, Russ Allbery",
    "license": "Apache-2.0",
    "install_requires": requires,
    "setup_requires": setup_requires,
    "tests_require": test_requires,
    "url": "https://github.com/dropbox/groupy",
    "classifiers": [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
}

setup(**kwargs)
