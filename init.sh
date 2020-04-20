rm -rf ./venv

python3 -m venv ./venv

find . -type d -name '*.egg-info' -exec rm -rf {} +

source activate.sh

python3 -m pip install --upgrade pip wheel
python3 -m pip install -e ".[dev]"
