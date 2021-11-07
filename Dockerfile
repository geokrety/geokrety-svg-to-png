FROM ubuntu:21.10

ARG TCE_VERSION=13.1.0

ENV APP_HOME /app
WORKDIR $APP_HOME

ENV TZ=Europe/Paris
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
 && apt-get update \
 && apt-get install -y \
        inkscape \
        libffi-dev \
        locales\
        python3-dev \
        python3-pip \
        ttf-bitstream-vera \
        wget \
 && locale-gen en_US.UTF-8 \
 && pip3 install Flask requests gevent \
 && wget -q https://github.com/eosrei/twemoji-color-font/releases/download/v$TCE_VERSION/TwitterColorEmoji-SVGinOT-Linux-$TCE_VERSION.tar.gz \
 && tar zxf TwitterColorEmoji-SVGinOT-Linux-$TCE_VERSION.tar.gz \
 && cd TwitterColorEmoji-SVGinOT-Linux-$TCE_VERSION \
 && ./install.sh \
 && cd .. \
 && rm -fr TwitterColorEmoji-SVGinOT-Linux-$TCE_VERSION TwitterColorEmoji-SVGinOT-Linux-$TCE_VERSION.tar.gz

COPY . $APP_HOME
COPY files/extensions/* /usr/share/inkscape/extensions/
CMD ["python3", "inkscape.py"]
