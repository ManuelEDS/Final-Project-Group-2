FROM python:3.8.13 AS base

ARG PYTHONPATH
ENV PYTHONPATH=$PYTHONPATH:/src/
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./ /src/

FROM base AS test
RUN ["python3", "-m", "pytest", "-v", "tests"]

FROM base AS build
CMD streamlit run --server.port 9090 app/image_classifier_app.py