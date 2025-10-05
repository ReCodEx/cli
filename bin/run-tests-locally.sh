# Runs the CI/CD tests locally.

# switch to the repository root
cd `dirname "$0"`/..

./bin/init.sh

source venv/bin/activate
rm ~/.local/share/recodex/context.yaml
python3 -m tests &
sleep 5
bats tests/tests.sh
