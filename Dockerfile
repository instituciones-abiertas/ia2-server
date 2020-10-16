FROM cambalab/python3-uno

RUN apt-get update && \
   apt-get install -y python-dev python-mysqldb gettext

ENV PYTHONUNBUFFERED 1

ENV HOME=/home/app
ENV APP_HOME=$HOME/web

RUN mkdir $HOME
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/uploads

ADD requirements/base.txt $APP_HOME
ADD requirements/production.txt $APP_HOME

ADD https://github.com/Cambalab/docker-compose-wait/releases/download/2.6.0/wait /wait
RUN chmod +x /wait

RUN pip install -U pip
RUN pip install -r $APP_HOME/production.txt

ADD . $APP_HOME
WORKDIR $APP_HOME
