FROM python:3.4-jessie

COPY requirements /requirements
COPY sources.list.jessie /etc/apt/sources.list
COPY Driver/chromedriver /usr/local/bin

RUN apt-get update && apt-get install -y \
    locales locales-all \
    xvfb gtk2-engines-pixbuf \
    xfonts-cyrillic xfonts-100dpi xfonts-75dpi xfonts-base xfonts-scalable

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN pip3 install -r /requirements/requirements.txt \
    && rm -rf /requirements

WORKDIR /project
VOLUME [ "/project" ]

CMD [ "bash", "runCase_headless.sh" ]