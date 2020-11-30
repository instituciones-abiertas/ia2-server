#!/bin/bash

/wait && \

echo "=> Starting Celery worker..." && \
celery --app=liberajus worker -D --concurrency=1 --loglevel=INFO && \

echo "=> Starting Django application..." && \
python manage.py runserver 0.0.0.0:8000 --settings=liberajus.settings.local
