FROM skiftcreative/supervisor:3.4
MAINTAINER Shawn McElroy <shawn@skift.io>

ENV SLACK_TOKEN "xoxb..."

RUN apk add --no-cache --virtual .build-deps  \
    bzip2-dev \
    gcc \
    libc-dev \
    linux-headers \
    make \
    ncurses-dev \
    openssl-dev \
    pax-utils \
    readline-dev \
    sqlite-dev \
    zlib-dev \
    libffi-dev

COPY . /deploy/app

RUN pip3 install -U pip setuptools

RUN pip3 install -U certifi
RUN pip3 install -r /deploy/app/requirements.txt
RUN cd /deploy/app \
    && python3 /deploy/app/setup.py install

RUN apk del .build-deps

COPY .docker/supervisord.conf /etc/supervisord.conf