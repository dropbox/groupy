#!/usr/bin/env python

import setuptools
from distutils.core import setup

execfile("groupy/version.py")

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

kwargs = {
    "name": "groupy",
    "version": str(__version__),
    "packages": ["groupy"],
    "description": "Python client library for Grouper",
    # PyPi, despite not parsing markdown, will prefer the README.md to the
    # standard README. Explicitly read it here.
    "long_description": open("README").read(),
    "author": "Gary M. Josack",
    "maintainer": "Gary M. Josack",
    "author_email": "gary@dropbox.com",
    "maintainer_email": "gary@dropbox.com",
    "license": "Apache",
    "install_requires": required,
    "url": "https://github.com/dropbox/groupy",
    "download_url": "https://github.com/dropbox/groupy/archive/master.tar.gz",
    "classifiers": [
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
}

setup(**kwargs)
