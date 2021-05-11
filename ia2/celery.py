import os
from .settings.base import CELERY_BROKER_URL, CELERY_ONCE
from celery import Celery

SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)

app = Celery("ia2", broker=CELERY_BROKER_URL)
app.config_from_object(SETTINGS_MODULE, namespace="CELERY")
app.conf.ONCE = CELERY_ONCE
app.autodiscover_tasks()
