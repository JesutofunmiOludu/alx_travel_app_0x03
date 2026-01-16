#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirement.txt

python manage.py collectstatic --noinput
python manage.py migrate
