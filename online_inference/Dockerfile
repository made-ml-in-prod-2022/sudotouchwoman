FROM python:3.8-slim

COPY ./ /app/
WORKDIR /app

RUN mkdir logs \
 && pip install --upgrade pip \
 && pip install -r requirements.txt \
 && pip install gunicorn

EXPOSE 5000
