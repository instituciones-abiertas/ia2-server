#!/bin/bash

echo "=> Compiling translations..."
python manage.py compilemessages --settings=liberajus.settings.local

echo "=> Starting Libreoffice headless service..."
/usr/bin/libreoffice --headless --nologo --nofirststartwizard --accept="socket,host=0.0.0.0,port=8001;urp" &

/wait && \
echo "=> Performing database migrations..." && \
python manage.py migrate --settings=liberajus.settings.local && \
python manage.py migrate --database=data_db --settings=liberajus.settings.local && \

echo "=> Loading fixtures..." && \
make django-load-fixtures && \

echo "=> Starting Django application..." && \
python manage.py runserver 0.0.0.0:8000 --settings=liberajus.settings.local