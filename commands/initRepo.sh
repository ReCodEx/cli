#!/bin/bash

# run the script from the root of the repository

if ! test -d ./venv; then
  echo "Initializing Python venv"
  python3.11 -m venv venv
  ./venv/bin/pip install -r requirements.txt
  PIP_EXTRA_INDEX_URL="https://test.pypi.org/simple/" ./venv/bin/pip install -e .
fi
