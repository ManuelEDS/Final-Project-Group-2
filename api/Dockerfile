FROM python:3.8.13 AS base

ARG PYTHONPATH
ENV PYTHONPATH=$PYTHONPATH:/src/
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./ /src/

FROM base AS build

CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000 main:app