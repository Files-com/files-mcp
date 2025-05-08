#!/usr/bin/env bash

# Create a temporary directory for the virtual environment
VENV_DIR=$(mktemp -d)
echo "Creating virtualenv in $VENV_DIR"

# Create and activate the virtualenv
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Execute running tests from same directory as current script
cd "$(dirname "$0")"

# Install dependencies
pip3 install .
pip3 install "flake8~=6.1.0" "black~=23.9.0" "pyright==1.1.400"

python3 -m black .
python3 -m flake8 files_com_mcp && python3 -m pyright && python3 -m unittest discover

# Deactivate and clean up
deactivate
rm -rf "$VENV_DIR"
echo "Cleaned up virtualenv"