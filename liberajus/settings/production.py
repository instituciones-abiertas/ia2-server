from .base import *  # noqas
import datetime
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")

DEBUG = os.environ.get("DEBUG", True)

# Use cached templates in production
TEMPLATES[0]["APP_DIRS"] = False
TEMPLATES[0]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    ),
]

# SSL required for session/CSRF cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

URL_SCHEME = "https"

MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

if os.environ.get("API_URL"):
    API_URL = os.environ.get("API_URL")

if os.environ.get("DOCKER_COMPOSE"):
    CELERY_BROKER_URL = os.environ.get("MY_APP_NAME_BROKER")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("LIBERAJUS_DB_NAME"),
            "USER": os.environ.get("LIBERAJUS_DB_USER"),
            "PASSWORD": os.environ.get("LIBERAJUS_DB_PASS"),
            "HOST": os.environ.get("LIBERAJUS_DB_HOST"),
            "PORT": 3306,
        },
        "data_db": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("LIBERAJUS_DB_DATA_NAME"),
            "USER": os.environ.get("LIBERAJUS_DB_DATA_USER"),
            "PASSWORD": os.environ.get("LIBERAJUS_DB_DATA_PASS"),
            "HOST": os.environ.get("LIBERAJUS_DB_DATA_HOST"),
            "PORT": 3306,
        },
    }

TIME_ZONE = "America/Buenos_Aires"

MEDIA_ROOT_TEMP_FILES = os.path.join(MEDIA_ROOT, "tmp/")
MEDIA_ROOT_ANONYMOUS_FILES = os.path.join(MEDIA_ROOT, "anonymous/")

LIBREOFFICE_HOST = os.environ.get("LIBREOFFICE_HOST")
LIBREOFFICE_PORT = os.environ.get("LIBREOFFICE_PORT")

LIBERAJUS_CLOUDFOLDER_STORE = os.environ.get("LIBERAJUS_CLOUDFOLDER_STORE")
LIBERAJUS_CLOUD_STORAGE_PROVIDER = os.environ.get("LIBERAJUS_CLOUD_STORAGE_PROVIDER")
LIBERAJUS_DROPBOX_TOKEN_APP = os.environ.get("LIBERAJUS_DROPBOX_TOKEN_APP")
LIBERAJUS_CREDENTIALS_DRIVE_PATH = os.environ.get("LIBERAJUS_CREDENTIALS_DRIVE_PATH")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=20),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

sentry_sdk.init(
    dsn=os.environ.get("SENRTY_DSN"),
    environment=os.environ.get("SENTRY_RELEASE"),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    debug=False,
)

LIBERAJUS_DISABLE_ENTITIES = os.environ.get("LIBERAJUS_DISABLE_ENTITIES")

## ML Model
LIBERAJUS_MODEL_FILE = os.environ.get("LIBERAJUS_MODEL_FILE")
