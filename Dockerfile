FROM python:3.7.4-alpine3.10

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "--log-level", "debug", "api:app"]