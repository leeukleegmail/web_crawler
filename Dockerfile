# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster


ARG container_name
ENV CONTAINER_NAME $container_name

WORKDIR /$CONTAINER_NAME

COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD [ "python3", "server.py"]
