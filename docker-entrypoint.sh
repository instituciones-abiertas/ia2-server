#!/bin/bash

echo "=> Performing database migrations..."
python manage.py migrate --settings=liberajus.settings.production
python manage.py migrate --database data_db --settings=liberajus.settings.production

echo "=> Collecting static files..."
python manage.py collectstatic --noinput --settings=liberajus.settings.production

echo "=> Compiling translations..."
python manage.py compilemessages --settings=liberajus.settings.production

# echo "=> Adding sections..."
# python manage.py loaddata apps/my_model/fixtures/3_some_property.json  --settings=applicationname.settings.production

echo "=> Starting Libreoffice headless"
/usr/bin/libreoffice --headless --nologo --nofirststartwizard --accept="socket,host=0.0.0.0,port=8001;urp" &

echo "=> Starting webserver..."
gunicorn --bind 0.0.0.0:8000 liberajus.wsgi:application
