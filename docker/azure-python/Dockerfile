FROM ubuntu:17.10

ARG DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

RUN apt-get update \
        && apt-get install -y --no-install-recommends apt-utils


RUN apt-get update \
        && apt-get install -y --no-install-recommends vim \
        && apt-get install -y python3-pip \
        && apt-get install -y freetds-dev