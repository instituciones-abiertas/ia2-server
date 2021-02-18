FROM cambalab/python3-uno

RUN apt-get update && \
   apt-get install -y python-dev python-mysqldb gettext

# Domain specific database arguments
ARG main_db_user
ARG main_db_password
ARG main_db_root_password
ARG main_db_name
ARG main_db_host
ARG main_db_port
# Data Extraction database arguments
ARG data_db_user
ARG data_db_password
ARG data_db_root_password
ARG data_db_name
ARG data_db_host
ARG data_db_port
# Django and third party services arguments
ARG secret_key
ARG dropbox_token
ARG disable_entities
ARG model_file
ARG test_model_file

# Domain specific database environment
ENV LIBERAJUS_DB_NAME=${main_db_name}
ENV LIBERAJUS_DB_USER=${main_db_user}
ENV LIBERAJUS_DB_PASS=${main_db_password}
ENV LIBERAJUS_DB_HOST=${main_db_host}
ENV LIBERAJUS_DB_PORT=${main_db_port}
# Data Extraction database environment
ENV LIBERAJUS_DB_DATA_NAME=${data_db_name}
ENV LIBERAJUS_DB_DATA_USER=${data_db_user}
ENV LIBERAJUS_DB_DATA_PASS=${data_db_password}
ENV LIBERAJUS_DB_DATA_HOST=${data_db_host}
ENV LIBERAJUS_DB_DATA_PORT=${data_db_port}

ENV WAIT_HOSTS=main_db:3306,data_db:3306
# Django and third party services environment
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY=${secret_key}
ENV LIBERAJUS_DROPBOX_TOKEN_APP=${dropbox_token}
ENV LIBERAJUS_DISABLE_ENTITIES=${disable_entities}
ENV LIBERAJUS_MODEL_FILE=${model_file}
ENV LIBERAJUS_TEST_MODEL_FILE=${test_model_file}

# Exposes Django server port
EXPOSE 8000

RUN mkdir /app

WORKDIR /app

# Copies development settings
COPY requirements/base.txt /app
COPY requirements/local.txt /app
COPY requirements/testing.txt /app

COPY . /app

# Installs development dependencies
RUN pip install -U pip
RUN pip install -r local.txt

# Configures Uno library
RUN cp /usr/lib/python3/dist-packages/uno.py /usr/local/lib/python3.7/site-packages/uno.py
RUN cp /usr/lib/python3/dist-packages/unohelper.py /usr/local/lib/python3.7/site-packages/unohelper.py

ADD . /app

# Adds the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait

RUN chmod +x /wait
