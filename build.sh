#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Si usas django-tailwind, necesitas instalar las dependencias de node
# y buildear el theme. Render tiene Node instalado por defecto.
python manage.py tailwind install
python manage.py tailwind build

python manage.py collectstatic --no-input
python manage.py migrate