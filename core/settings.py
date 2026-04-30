import os
import logging
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
import cloudinary

logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Dirección de los templates
TEMPLATES_DIRS = BASE_DIR / 'core' / 'templates'

# Cargar variables de entorno desde .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-key-para-desarrollo")

# SECURITY WARNING: don't run with debug turned on in production!
# Busca el valor en el entorno, si no existe (en la PC), por defecto es True
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

if not os.environ.get("SECRET_KEY") and not DEBUG:
    raise ValueError("¡La SECRET_KEY no está configurada en las variables de entorno!")

ALLOWED_HOSTS = ['booking-manager-django.onrender.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cloudinary',
    'cloudinary_storage',
    'django_extensions',
    'tailwind',
    'theme',
    'django_browser_reload',
    
    'core',
    'users',
    'zones',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIRS,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# URL base que se usará en el navegador (ej: /media/profile_pictures/foto.jpg)
MEDIA_URL = '/media/'

# Carpeta física en tu proyecto donde se guardarán (se creará automáticamente)
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# A dónde va el usuario después de loguearse
LOGIN_REDIRECT_URL = 'profile'

# A dónde va el usuario después de cerrar sesión
LOGOUT_REDIRECT_URL = 'home'

# A dónde mandamos a alguien que intenta entrar a una página protegida sin estar logueado
LOGIN_URL = 'login'

# Configuración para el envío de correos electrónicos (usado en el formulario de contacto)
'''Mail is sent using the SMTP host and port specified in the EMAIL_HOST and EMAIL_PORT settings. The EMAIL_HOST_USER and EMAIL_HOST_PASSWORD settings, if set, are used to authenticate to the SMTP server, and the EMAIL_USE_TLS and EMAIL_USE_SSL settings control whether a secure connection is used.'''

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get("SECRET_EMAIL", "django-insecure-default-key-para-desarrollo")
EMAIL_HOST_PASSWORD = os.environ.get("SECRET_KEY_EMAIL", "django-insecure-default-key-para-desarrollo")
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_TIMEOUT = 5  # Segundos. Evita que el worker de Gunicorn haga timeout (30s) si el servidor SMTP no responde

# Configuración de Cloudinary para almacenamiento de archivos media en producción
# Cloudinary lee automáticamente CLOUDINARY_URL del entorno
# Formato esperado: cloudinary://api_key:api_secret@cloud_name

try:
    cloudinary.config()
    logger.info("Cloudinary configurado automáticamente")
except Exception as e:
    logger.warning(f"No se pudo configurar Cloudinary: {e}")

# STORAGES: API correcta desde Django 5.1+ / 6.x
# DEFAULT_FILE_STORAGE y STATICFILES_STORAGE están deprecadas y son ignoradas
if DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }

# Constante para Tailwind
TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = [
    "127.0.0.1",
]
