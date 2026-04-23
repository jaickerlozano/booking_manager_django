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

# Envuelve la aplicación con WhiteNoise para servir archivos estáticos
application = WhiteNoise(application)

# Configurar WhiteNoise solo para archivos estáticos (CSS, JS, etc)
# Los archivos media son servidos por Django en desarrollo y por Cloudinary en producción
application.add_files(settings.STATIC_ROOT, prefix=settings.STATIC_URL)
