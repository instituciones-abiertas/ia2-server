#!/bin/bash

/wait && \

echo "=> Starting Celery worker..." && \
celery --app=ia2 worker -D --concurrency=1 --loglevel=INFO && \

echo "=> Starting Django application..." && \
python manage.py runserver 0.0.0.0:8000 --settings=ia2.settings.local
