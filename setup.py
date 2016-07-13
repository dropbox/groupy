#!/usr/bin/env python

from setuptools import setup

execfile("groupy/version.py")

kwargs = {
    "name": "groupy",
    "version": str(__version__),  # noqa
    "packages": ["groupy"],
    "description": "Python client library for Grouper",
    "author": "Gary M. Josack, Mark Smith, Herbert Ho, Luke Faraone",
    "license": "Apache-2.0",
    "install_requires": [
        "clowncar",
        "tornado>=3.2",
    ],
    "setup_requires": [
        "flake8==2.5.0",
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
