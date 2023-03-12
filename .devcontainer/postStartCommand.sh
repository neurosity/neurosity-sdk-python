#!/bin/bash

# Runs every time a new dev container is started.

# Suppress 'detected dubious ownership' errors for git commands.
# Must be run every time the container starts since VSCode copies
# $HOME/.gitconfig of host machine to container on every start.
git config --global --add safe.directory '/workspaces'

# Update pip
pip install --upgrade pip

# analytics container setup
#source bin/activate-hermit
#pip install virtualenv
#virtualenv analytics
