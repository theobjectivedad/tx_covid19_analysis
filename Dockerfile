FROM selenium/standalone-chrome:latest

USER root

RUN apt-get update && \
    apt-get install -y python3-pip && \
    rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY requirements.txt /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

ENV PROJECT_DIR=/opt/project
RUN mkdir ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}