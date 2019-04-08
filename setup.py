#!/usr/bin/env python

import sys

from setuptools import setup

# Define __version__.  This is equivalent to execfile but works in Python 3.
with open("groupy/version.py", "r") as version:
    code = compile(version.read(), "groupy/version.py", "exec")
    exec(code)

setup_requires = []
if "flake8" in sys.argv:
    setup_requires += ["flake8==3.7.5", "flake8-import-order==0.18"]
if "test" in sys.argv:
    setup_requires += ["pytest-runner"]

kwargs = {
    "name": "groupy",
    "version": __version__,  # noqa
    "packages": ["groupy"],
    "description": "Python client library for Grouper",
    "author": "Gary M. Josack, Mark Smith, Herbert Ho, Luke Faraone",
    "license": "Apache-2.0",
    "install_requires": [
        "clowncar",
        "tornado==4.5.3",
    ],
    "setup_requires": setup_requires,
    "tests_require": [
        "flake8==3.7.5",
        "flake8-import-order==0.18",
        "pytest>=2.6",
        "pytest-runner",
        "mock>=1.0",
    ],
    "url": "https://github.com/dropbox/groupy",
    "classifiers": [
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
}

setup(**kwargs)
