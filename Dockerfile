FROM python:3.7.4-alpine3.10

COPY api /application/api
ADD app /application/api/app
COPY requirements.txt /application

WORKDIR /application/api

RUN pip install -r /application/requirements.txt
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "--log-level", "debug", "api:app", "--timeout", "1200"]