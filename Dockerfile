FROM skiftcreative/supervisor:3.4
MAINTAINER Shawn McElroy <shawn@skift.io>

ENV SLACK_TOKEN "xoxb..."

COPY . /deploy/app

RUN pip3 install -U pip setuptools

RUN pip3 install -r /deploy/app/requirements.txt \
    && cd /deploy/app \
    && python3 /deploy/app/setup.py install

COPY .docker/supervisord.conf /etc/supervisord.conf