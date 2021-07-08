FROM python:3.9-slim

COPY requirements.pip /tmp/requirements.pip
RUN pip3 install -U -r /tmp/requirements.pip

COPY *.py ./
