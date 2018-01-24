FROM ubuntu

# Follow APT advice from
#    https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/
RUN set -ex; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install apt-utils; \
    DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install \
      apt-transport-https \
      ca-certificates \
      curl \
      gcc \
      gnupg2 \
      libffi-dev \
      libssl-dev \
      locales \
      lsb-release \
      python3 \
      python3-dev \
      python3-pip \
      software-properties-common \
    ; \
    locale-gen en_US.UTF-8; \
    ln -s /usr/bin/python3 /usr/bin/python; \
    ln -s /usr/bin/pip3 /usr/bin/pip; \
    pip install --upgrade pip setuptools; \
    :

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

ADD bin/limbo /app/bin/limbo
ADD limbo /app/limbo/
ADD setup.py /app/
RUN set -ex; \
    python setup.py install; \
    rm -rf build dist limbo.egg-info; \
    :

ADD test /app/test/

ENTRYPOINT ["/usr/local/bin/limbo"]
