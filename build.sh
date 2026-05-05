#!/usr/bin/env bash

set -o errexit  # ⛔ detiene si algo falla

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

# 👇 Crear superusuario automáticamente
python manage.py shell << END
from django.contrib.auth.models import User

username = "fallen"
email = "fallenpf@gmail.com"
password = "Fallen123."

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
END