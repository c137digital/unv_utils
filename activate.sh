find . -type f -name '*.py[co]' -delete
find . -type d -name '__pycache__' -exec rm -rf {} +

source ./venv/bin/activate
