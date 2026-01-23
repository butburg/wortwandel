#!/bin/bash

# Create directories if they do not exist
mkdir -p data_output
mkdir -p data_input


# Dynamically add user Python bin directory to PATH
#PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
#export PATH="$HOME/Library/Python/$PYTHON_VERSION/bin:$PATH"

# Install pipenv and project dependencies
pip install pipenv
pipenv install
