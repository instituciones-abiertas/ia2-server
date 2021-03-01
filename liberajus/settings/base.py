"""
Django settings for liberajus project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dj_database_url
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", True)

ALLOWED_HOSTS = []


# Application definition

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


THIRD_PARTY_APPS = ["rest_framework", "rest_framework.authtoken", "private_storage"]

PROJECT_APPS = [
    "apps.accounts",
    "apps.i18n_switcher",
    "apps.entity",
    "apps.data",
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "liberajus.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "liberajus.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(env="DATABASE_URL"),
    "data_db": dj_database_url.config(env="DATABASE_DATA_URL"),
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

TIME_ZONE = "UTC"

LANGUAGE_CODE = "es"

LANGUAGES = (
    ("en", _("english")),
    ("es", _("spanish")),
)

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static/")
STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


# Custom user model
AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

DATABASE_ROUTERS = ["liberajus.router.DBRouter"]

URL_SCHEME = "http"

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "uploads/")
MEDIA_URL = "/uploads/"

LOCALE_PATHS = [os.path.join(os.path.dirname(BASE_DIR), "locale/")]

API_URL = "http://localhost:8000"


PRIVATE_STORAGE_ROOT = os.path.join(os.path.dirname(BASE_DIR), "uploads/")
PRIVATE_STORAGE_ANONYMOUS_FOLDER = os.path.join(os.path.dirname(PRIVATE_STORAGE_ROOT), "anonymous/")
PRIVATE_STORAGE_ANONYMOUS_URL = "anonymous/"
PRIVATE_STORAGE_AUTH_FUNCTION = "private_storage.permissions.allow_superuser"

MODELS_PATH = f"{os.path.abspath(os.path.dirname(__name__))}/custom_models"
LIBERAJUS_DISABLE_ENTITIES = []

# Celery Configuration Options

# Default options for local and testing environments
# This is needed since celery.py imports settings from .base
BROKER_HOST = "broker"
BROKER_USER = "user"
BROKER_PASSWORD = "password"
BROKER_PORT = 5672
CELERY_BROKER_URL = f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}"
REDIS_HOST = "redis"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379/1"

# Production and local environment
if os.environ.get("DOCKER_COMPOSE"):
    BROKER_HOST = os.environ.get("BROKER_HOST")
    BROKER_USER = os.environ.get("BROKER_USER")
    BROKER_PASSWORD = os.environ.get("BROKER_PASSWORD")
    BROKER_PORT = os.environ.get("BROKER_PORT")
    CELERY_BROKER_URL = f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}"
    REDIS_HOST = os.environ.get("REDIS_HOST")
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379/1"

# Staging environment
if os.environ.get("RABBITMQ_URL"):
    CELERY_BROKER_URL = os.environ.get("RABBITMQ_URL")
if os.environ.get("REDIS_URL"):
    CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")

# Other options
CELERY_RESULT_PERSISTENT = False
CELERY_TIMEZONE = "America/Argentina/Buenos_Aires"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_ONCE = {
    "backend": "celery_once.backends.Redis",
    "settings": {
        "blocking": True,
        "blocking_timeout": 10,
        "url": CELERY_RESULT_BACKEND,
        "default_timeout": CELERY_TASK_TIME_LIMIT,
    },
}

# OODocument Configuration

LIBREOFFICE_HOST = "0.0.0.0"
LIBREOFFICE_PORT = 8001
HEADER_EXTRACT_ENABLE = os.environ.get("HEADER_EXTRACT_ENABLE")
if os.environ.get("OODOCUMENT_NEIGHBOR_CHARS_SCAN"):
    NEIGHBOR_CHARS_SCAN = int(os.environ.get("OODOCUMENT_NEIGHBOR_CHARS_SCAN"))
else:
    NEIGHBOR_CHARS_SCAN = 20  # Valor default si no viene seteada la variable

# Publicador Configuration

LIBERAJUS_CLOUDFOLDER_STORE = os.environ.get("LIBERAJUS_CLOUDFOLDER_STORE")
LIBERAJUS_CLOUD_STORAGE_PROVIDER = os.environ.get("LIBERAJUS_CLOUD_STORAGE_PROVIDER")
LIBERAJUS_DROPBOX_TOKEN_APP = os.environ.get("LIBERAJUS_DROPBOX_TOKEN_APP")
LIBERAJUS_CREDENTIALS_DRIVE_PATH = os.environ.get("LIBERAJUS_CREDENTIALS_DRIVE_PATH")

## Publicador Error types

ERROR_TEXT_FILE_TYPE = "El tipo de archivo no es soportado por el sistema"
ERROR_OODOCUMENT_NOT_WORKING = "El servicio de transcripcion no esta funcionando"
ERROR_NAME_TOO_LONG = "El nombre del archivo excede los 150 caracteres"
ERROR_ACT_FILE_NOT_FOUND = "No envio un archivo"
ERROR_DROPBOX_CREDENTIALS = "Las credenciales de dropbox estan expiradaso o son incorrectas"
ERROR_DRIVE_CREDENTIALS = "Las credenciales de Drive estan expiradas o son incorrectas"
ERROR_ACT_NOT_EXIST = "No existe el acta que se quiere acceder"
ERROR_STORAGE_FILE_NOT_EXIST = "El archivo no se encuentra disponible"
ERROR_DRIVE_CREDENTIALS_NOT_FOUND = "No se encuentran las credenciales en el servidor"
ERROR_STORAGE_CLOUD_FOLDER_NOT_EXIST = "No existe la carpeta configurada en el servidor"
