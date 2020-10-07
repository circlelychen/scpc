FROM python:3.6-slim-buster

MAINTAINER Hao-Yuan Chen <truecirclely@gmail.com>

ENV PYTHONIOENCODING UTF-8


# copy require
COPY ./req.txt ./

# Install required packages
RUN pip install \
    --no-cache-dir \
    --requirement ./req.txt

RUN mkdir -p /scpc
WORKDIR /scpc
