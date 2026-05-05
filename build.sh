#!/usr/bin/env bash

set -o errexit  # ⛔ detiene si algo falla

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate