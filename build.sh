#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Si usas django-tailwind, necesitas instalar las dependencias de node
# y buildear el theme. Render tiene Node instalado por defecto.
python manage.py tailwind install
python manage.py tailwind build

# Recolectar archivos estáticos (con más tolerancia a errores)
python manage.py collectstatic --no-input --clear --ignore=media --ignore=.gitignore

# Ejecutar migraciones
python manage.py migrate