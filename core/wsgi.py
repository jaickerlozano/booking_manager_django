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

# Envuelve la aplicación con WhiteNoise para servir archivos estáticos y media
application = WhiteNoise(application)

# Configurar WhiteNoise para servir archivos estáticos en la URL STATIC_URL
application.add_files(settings.STATIC_ROOT, prefix=settings.STATIC_URL)

# Configurar WhiteNoise para servir archivos media en la URL MEDIA_URL
application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)
