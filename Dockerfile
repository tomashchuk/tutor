# syntax=docker/dockerfile:1
FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN #apk update && apk add libpq-dev gcc
RUN apk add --no-cache gcc musl-dev python3-dev
RUN pip install -r requirements.txt
COPY . /code/