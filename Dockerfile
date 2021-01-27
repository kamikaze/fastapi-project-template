FROM python:3.9.1-slim as build-image

WORKDIR /usr/local/bin/cl

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y curl ca-certificates gnupg
RUN curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get install -y gcc g++ make postgresql-server-dev-all libpq-dev libffi-dev git cargo

COPY ./ /tmp/build
COPY src/template_project/db/migrations ./migrations/
COPY src/template_project/db/alembic.ini ./alembic.ini

RUN  (cd /tmp/build \
     && python3 -m venv py3env-dev \
     && . py3env-dev/bin/activate \
     && python3 -m pip install -U -r requirements_dev.txt \
     && python3 setup.py bdist_wheel)


RUN  export APP_HOME=/usr/local/bin/cl \
     && (cd $APP_HOME \
         && python3 -m venv py3env \
         && . py3env/bin/activate \
         && python3 -m pip install -U pip \
         && python3 -m pip install -U setuptools \
         && python3 -m pip install -U wheel \
         && python3 -m pip install -U template_project --find-links=/tmp/build/dist)


FROM python:3.9.1-slim

ENV  PYTHONPATH=/usr/local/bin/cl

RUN  mkdir -p /usr/local/bin/cl \
     && apt-get update \
     && apt-get -y upgrade \
     && apt-get install -y libpq-dev

WORKDIR /usr/local/bin/cl

COPY --from=build-image /usr/local/bin/cl/ ./

RUN  groupadd -r appgroup \
     && useradd -r -G appgroup -d /home/appuser appuser \
     && install -d -o appuser -g appgroup /usr/local/bin/cl/logs

USER  appuser

EXPOSE 8080


CMD ["/usr/local/bin/cl/py3env/bin/python3", "-m", "uvicorn", "template_project.api.http:app", "--host", "0.0.0.0", \
     "--port", "8080"]

