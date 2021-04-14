from .base import *  # noqa

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_ia2_backend",
    },
    "data_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_ia2_data_backend",
    },
}

SECRET_KEY = "camba420"


# Celery Configuration Options

BROKER_HOST = "broker"
BROKER_USER = "user"
BROKER_PASSWORD = "password"
BROKER_PORT = 5672
CELERY_BROKER_URL = f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}"
REDIS_HOST = "redis"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379/1"

CELERY_RESULT_PERSISTENT = False
CELERY_TIMEZONE = "America/Argentina/Buenos_Aires"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

MEDIA_ROOT_TEMP_FILES = os.path.join(MEDIA_ROOT, "test_tmp/")
MEDIA_ROOT_ANONYMOUS_FILES = os.path.join(MEDIA_ROOT, "test_anonymous/")

# OODocument Configuration

LIBREOFFICE_HOST = "0.0.0.0"
LIBREOFFICE_PORT = 8001

PUBLICADOR_CLOUDFOLDER_STORE = "ia2_test_directory"
PUBLICADOR_CLOUD_STORAGE_PROVIDER = "dropbox"
PUBLICADOR_DROPBOX_TOKEN_APP = os.environ.get("PUBLICADOR_DROPBOX_TOKEN_APP")
PUBLICADOR_CREDENTIALS_DRIVE_PATH = os.environ.get("PUBLICADOR_CREDENTIALS_DRIVE_PATH")

## ML Model
IA2_MODEL_FILE = os.environ.get("IA2_TEST_MODEL_FILE")
