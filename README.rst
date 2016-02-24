======
groupy
======

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

New versions will be updated to PyPI pretty regularly so it should be as easy
as:

.. code:: bash

    pip install groupy
