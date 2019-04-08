#!/bin/bash

set -eux

# Tests run under Python 2.
if [[ "$TRAVIS_PYTHON_VERSION" == 2* ]]; then
    pytest -x -v
    flake8
fi

# Tests run under Python 3.
if [[ "$TRAVIS_PYTHON_VERSION" == 3* ]]; then
    pytest -x -v
    mypy .
    black --check .
    flake8
fi
