FROM python:3.7.4-alpine3.10

COPY api /application/api
ADD app /application/api/app
COPY requirements.txt /application

WORKDIR /application/api

RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r /application/requirements.txt
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "api:app", "--log-level", "debug", "--timeout", "1200"]
