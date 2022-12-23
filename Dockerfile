FROM python:3.11-slim as build-image

WORKDIR /usr/local/app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y curl ca-certificates gnupg
RUN curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get install -y gcc g++ make postgresql-server-dev-all libpq-dev libffi-dev git cargo

COPY ./ /tmp/build
COPY src/fastapi_project_template/db/migrations ./migrations/
COPY src/fastapi_project_template/db/alembic.ini ./alembic.ini

RUN  (cd /tmp/build \
     && python3 -m venv venv-dev \
     && . venv-dev/bin/activate \
     && python3 -m pip install -U -r requirements_dev.txt \
     && python3 setup.py bdist_wheel)


RUN  export APP_HOME=/usr/local/app \
     && (cd $APP_HOME \
         && python3 -m venv venv \
         && . venv/bin/activate \
         && python3 -m pip install -U pip \
         && python3 -m pip install -U setuptools \
         && python3 -m pip install -U wheel \
         && python3 -m pip install -U fastapi_project_template --find-links=/tmp/build/dist)


FROM python:3.11-slim

ENV  PYTHONPATH=/usr/local/app

RUN  mkdir -p /usr/local/app \
     && apt-get update \
     && apt-get -y upgrade \
     && apt-get install -y libpq-dev

WORKDIR /usr/local/app

COPY --from=build-image /usr/local/app/ ./

RUN  groupadd -r appgroup \
     && useradd -r -G appgroup -d /home/appuser appuser \
     && install -d -o appuser -g appgroup /usr/local/app/logs

USER  appuser

EXPOSE 8080


CMD ["/usr/local/app/venv/bin/python3", "-m", "uvicorn", "fastapi_project_template.api.http:app", \
     "--host", "0.0.0.0", "--port", "8080"]
