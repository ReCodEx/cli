#!/bin/sh

PIP_EXTRA_INDEX_URL="https://test.pypi.org/simple/" ./venv/bin/python3 -m build
./venv/bin/python3 -m twine upload --repository testpypi dist/*
