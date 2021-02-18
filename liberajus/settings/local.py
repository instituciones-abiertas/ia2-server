import os
import datetime
from importlib import import_module
from .base import *

DEBUG = True
TEMPLATES[0]["OPTIONS"]["debug"] = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("LIBERAJUS_DB_NAME"),
        "USER": os.environ.get("LIBERAJUS_DB_USER"),
        "PASSWORD": os.environ.get("LIBERAJUS_DB_PASS"),
        "HOST": os.environ.get("LIBERAJUS_DB_HOST"),
        "PORT": 3306,
        "CONN_MAX_AGE": 3600,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
    "data_db": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("LIBERAJUS_DB_DATA_NAME"),
        "USER": os.environ.get("LIBERAJUS_DB_DATA_USER"),
        "PASSWORD": os.environ.get("LIBERAJUS_DB_DATA_PASS"),
        "HOST": os.environ.get("LIBERAJUS_DB_DATA_HOST"),
        "PORT": 3306,
        "CONN_MAX_AGE": 3600,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
}

INTERNAL_IPS = ["127.0.0.1"]
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "django_extensions",
]

# Use vanilla StaticFilesStorage to allow tests to run outside of tox easily
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

SECRET_KEY = "applicationname"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Django debug toolbar - show locally unless DISABLE_TOOLBAR is enabled with environment vars
# eg. DISABLE_TOOLBAR=1 ./manage.py runserver
if not os.environ.get("DISABLE_TOOLBAR"):
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE


if os.environ.get("ENABLE_PYINSTRUMENT"):
    MIDDLEWARE = [
        "pyinstrument.middleware.ProfilerMiddleware",
    ] + MIDDLEWARE
    PYINSTRUMENT_PROFILE_DIR = "profiles"


if os.environ.get("API_URL"):
    API_URL = os.environ.get("API_URL")

TIME_ZONE = "America/Buenos_Aires"

MEDIA_ROOT_TEMP_FILES = os.path.join(MEDIA_ROOT, "tmp/")
MEDIA_ROOT_ANONYMOUS_FILES = os.path.join(MEDIA_ROOT, "anonymous/")


LIBREOFFICE_HOST = "0.0.0.0"
LIBREOFFICE_PORT = 8001

LIBERAJUS_CLOUDFOLDER_STORE = "liberajus-demo"
LIBERAJUS_CLOUD_STORAGE_PROVIDER = "dropbox"
LIBERAJUS_DROPBOX_TOKEN_APP = os.environ.get("LIBERAJUS_DROPBOX_TOKEN_APP")
LIBERAJUS_CREDENTIALS_DRIVE_PATH = "./credentials.json"


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


LIBERAJUS_DISABLE_ENTITIES = os.environ.get("LIBERAJUS_DISABLE_ENTITIES")

## ML Model
LIBERAJUS_MODEL_FILE = os.environ.get("LIBERAJUS_MODEL_FILE")
