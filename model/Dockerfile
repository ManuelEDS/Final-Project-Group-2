FROM python:3.9 AS base

ARG PYTHONPATH
ENV PYTHONPATH=$PYTHONPATH:/src/
ENV PYTHONUNBUFFERED=1

ADD requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./ /src/

WORKDIR /src

FROM base as build
ENTRYPOINT ["python3", "/src/ml_service.py"]

