#!/usr/bin/env python

from setuptools import setup

execfile("groupy/version.py")

kwargs = {
    "name": "groupy",
    "version": str(__version__),  # noqa
    "packages": ["groupy"],
    "description": "Python client library for Grouper",
    # TODO(lfaraone): Check whether this is still needed for PyPI.
    "long_description": open("README.rst").read(),
    "author": "Gary M. Josack",
    "maintainer": "Gary M. Josack",
    "author_email": "gary@dropbox.com",
    "maintainer_email": "gary@dropbox.com",
    "license": "Apache-2.0",
    "install_requires": [
        "clowncar",
        "tornado>=3.2",
    ],
    "setup_requires": [
        "flake8",
        "pytest-runner",
    ],
    "tests_require": [
        "pytest>=2.6",
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
