#!/usr/bin/env bash

# Exit on non-zero status
set -e

# Execute running tests from same directory as current script
cd "$(dirname "$0")"

pyenv local 3.11.4

# Install dependencies
pip3 install .
pip3 install "flake8~=6.1.0" "black~=23.9.0" "pyright==1.1.400"

python3 -m black .

python3 -m flake8 files_com_mcp
python3 -m pyright
python3 -m unittest discover

pyenv local --unset