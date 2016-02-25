FROM skiftcreative/supervisor:3.4
MAINTAINER Shawn McElroy <shawn@skift.io>

ENV SLACK_TOKEN "xoxb..."

COPY . /deploy/app

RUN pip3 install -U pip

RUN pip3 install -r /deploy/app/requirements.txt \
    && python setup.py install

COPY docker/supervisord.conf /etc/supervisord.conf