#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# installing requirements
pip3 install -r requirements.txt

# Collect static files
echo "Collecting static files"
python3 manage.py collectstatic --noinput

# Create directory for build files if it doesn't exist
mkdir -p staticfiles_build

# Copy static files to the build directory
cp -r staticfiles/ staticfiles_build/

