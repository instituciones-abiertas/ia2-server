#!/bin/bash

echo "=> Performing database migrations..."
python manage.py migrate --settings=liberajus.settings.production
python manage.py migrate --database data_db --settings=liberajus.settings.production

echo "=> Collecting static files..."
python manage.py collectstatic --noinput --settings=liberajus.settings.production

echo "=> Compiling translations..."
python manage.py compilemessages --settings=liberajus.settings.production

echo "=> Adding entity fixtures..."
python manage.py loaddata apps/entity/fixtures/1_entity.json --settings=liberajus.settings.production
echo "=> Adding initial learning model fixtures..."
python manage.py loaddata apps/entity/fixtures/2_initial_learning_models.json --settings=liberajus.settings.production
echo "=> Adding initial accounts fixtures..."
python manage.py loaddata apps/accounts/fixtures/2_superuser_accounts.json --settings=liberajus.settings.production

echo "=> Starting Libreoffice headless"
/usr/bin/libreoffice --headless --nologo --nofirststartwizard --accept="socket,host=0.0.0.0,port=8001;urp" &

echo "=> Starting webserver..."
gunicorn --bind 0.0.0.0:8000 liberajus.wsgi:application
