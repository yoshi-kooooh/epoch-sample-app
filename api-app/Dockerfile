FROM    ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NOWARNINGS yes

WORKDIR /tmp

RUN apt-get -y update   \
&&  apt-get -y upgrade  \
&&  apt-get -y install \
    locales \
    curl \
    python3-distutils \
    wget \
    unzip \
&&  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
&&  python3 get-pip.py \
&&  pip install -U pip \
&&  pip install -U flask-cors \
&&  pip install requests \
&&  python3 -m pip install Flask \
&&  python3 -m pip install pytz \
&&  python3 -m pip install markdown


WORKDIR /app

COPY ./api-app /app

CMD ["python3", "/app/goods.py"]

