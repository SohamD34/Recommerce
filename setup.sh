#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define the virtual environment directory
VENV_DIR="venv"

# Check if Python 3.11 is installed
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11 is not installed. Please install it and try again."
    exit 1
fi

# Create the virtual environment
echo "Creating virtual environment in $VENV_DIR..."
python3.11 -m venv $VENV_DIR

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found. Please make sure it exists in the current directory."
    deactivate
    exit 1
fi

# Install packages from requirements.txt
echo "Installing packages from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. Virtual environment is ready."