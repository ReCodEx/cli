# Runs the CI/CD tests locally.

./commands/initRepo.sh

source venv/bin/activate
rm ~/.local/share/recodex/context.yaml
python3 -m tests &
sleep 5
bats tests/tests.sh
