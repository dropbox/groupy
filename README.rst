======
groupy
======

Deprecation
-----------

The Grouper/Groupy projects have been deprecated. You may continue to use and maintain forks of the project, but the Dropbox team will no longer contribute to this repository.

Description
-----------

Python client library for interfacing with the Grouper API server.

Quickstart
----------

Super basic...

.. code:: python

    from groupy.client import Groupy
    grclient = Groupy('127.0.0.1:8990')
    for user in grclient.users:
        print user
    for permission in grclient.users.get('zorkian'):
        print permission

Installation
------------

To pull the latest version from PyPI:

.. code:: bash

    pip install groupy
