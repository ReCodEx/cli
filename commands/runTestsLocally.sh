# Runs the CI/CD tests locally.

if ! test -d ./venv; then
  echo "Initializing Python venv"
  python3.11 -m venv venv
  ./venv/bin/pip install -r requirements.txt
  PIP_EXTRA_INDEX_URL="https://test.pypi.org/simple/" ./venv/bin/pip install -e .
fi

source venv/bin/activate
rm ~/.local/share/recodex/context.yaml
python3 -m tests &
sleep 5
bats tests/tests.sh
