FROM python:3.12-slim-bookworm as build-image

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y curl ca-certificates gnupg
RUN curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt update && \
    apt install -y --no-install-recommends gcc g++ make postgresql-server-dev-all libpq-dev libffi-dev git cargo pkg-config && \
    apt autoremove --purge -y && \
    apt clean

COPY requirements.txt .
RUN python3 -m pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY --from=build-image /app/wheels /wheels

RUN pip install --no-cache /wheels/*

RUN  groupadd -r appgroup \
     && useradd -r -G appgroup -d /home/appuser appuser \
     && install -d -o appuser -g appgroup /usr/local/app/logs

USER  appuser

COPY --chown=appuser src/fastapi_project_template ./fastapi_project_template/

EXPOSE 8000

ENTRYPOINT ["python3", "-m", "fastapi_project_template"]
