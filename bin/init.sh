#!/bin/bash

# switch to the repository root
cd `dirname "$0"`/..

if ! test -d ./venv; then
  echo "Initializing Python venv"
  python3 -m venv venv
  ./venv/bin/pip install -r requirements.txt
  ./venv/bin/pip install -e .
fi
