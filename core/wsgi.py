"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Obtiene la aplicación WSGI estándar de Django
application = get_wsgi_application()

# Envuelve la aplicación con WhiteNoise.
# Primero, le decimos que sirva los archivos estáticos desde STATIC_ROOT (los que recoge `collectstatic`).
application = WhiteNoise(application, root=settings.STATIC_ROOT)

# Luego, añadimos la regla para servir los archivos de medios desde MEDIA_ROOT en la URL MEDIA_URL.
application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)
