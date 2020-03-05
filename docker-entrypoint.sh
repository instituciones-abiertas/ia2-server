#!/bin/bash

echo "=> Performing database migrations..."
python manage.py migrate --settings=applicationname.settings.production

echo "=> Collecting static files..."
python manage.py collectstatic --noinput --settings=applicationname.settings.production

echo "=> Compiling translations..."
python manage.py compilemessages --settings=applicationname.settings.production

# echo "=> Adding sections..."
# python manage.py loaddata apps/my_model/fixtures/3_some_property.json  --settings=applicationname.settings.production

echo "=> Starting webserver..."
gunicorn --bind 0.0.0.0:8000 applicationname.wsgi:application
