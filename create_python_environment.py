#!/bin/bash



echo "Creating enviroment..."
python3 -m venv $(pwd)/.env && \
	echo "  Done." || echo "  Error!"

echo "Activating environment..."
source $(pwd)/.env/bin/activate && \
	echo "  Done." || echo "  Error!"

echo "Updating pip packages..."
pip3 install --upgrade pip setuptools > /dev/null 2>&1 && \
	pip3 install pylint > /dev/null 2>&1 && \
	echo "  Done." || echo "  Error!"

if [[ $# -gt 0 ]] ; then
	echo "Installing user required packages..." && \
	        pip3 install "$@" > /dev/null 2>&1 && \
        	echo "  Done." || echo "  Error!"
fi
