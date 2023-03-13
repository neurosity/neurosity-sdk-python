#!/bin/bash

# Runs every time a new dev container is started.

# Suppress 'detected dubious ownership' errors for git commands.
# Must be run every time the container starts since VSCode copies
# $HOME/.gitconfig of host machine to container on every start.
git config --global --add safe.directory '/workspaces'

# Update pip
echo "Updating pip"
pip install --upgrade pip

echo "Installing requirements"
pip install -r requirements.txt

echo "Installing development requirements"
pip install -r dev-requirements.txt

echo "Configuring neurosity package for development"
pip install -e .

echo "Done with post start commands"
