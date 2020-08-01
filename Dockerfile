FROM ubuntu:groovy

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
 && wget -q https://github.com/eosrei/twemoji-color-font/releases/download/v12.0.1/TwitterColorEmoji-SVGinOT-Linux-12.0.1.tar.gz \
 && tar zxf TwitterColorEmoji-SVGinOT-Linux-12.0.1.tar.gz \
 && cd TwitterColorEmoji-SVGinOT-Linux-12.0.1 \
 && ./install.sh \
 && cd .. \
 && rm -fr TwitterColorEmoji-SVGinOT-Linux-12.0.1 TwitterColorEmoji-SVGinOT-Linux-12.0.1.tar.gz

COPY . $APP_HOME
COPY files/extensions/* /usr/share/inkscape/extensions/

CMD ["python3", "inkscape.py"]
