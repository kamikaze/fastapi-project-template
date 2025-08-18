ARG BASE_REGISTRY=docker.io/library
FROM ${BASE_REGISTRY}/python:3.13-slim-trixie AS build-image

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /build

RUN if [ -z "$ARCH" ]; then ARCH="$(uname -m)"; fi && \
    apt update && \
    apt upgrade -y && \
    apt install -y curl ca-certificates gnupg2 && \
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg && \
    echo "deb https://apt.postgresql.org/pub/repos/apt trixie-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    apt update && \
    apt install -y --no-install-recommends gcc g++ make cmake postgresql-server-dev-17 libpq-dev libpq5 libffi-dev git cargo pkg-config && \
    python -m pip install -U setuptools pip wheel && \
    curl https://sh.rustup.rs -sSf | bash -s -- -y && \
    mkdir -p /usr/lib/linux-gnu && \
    cp /usr/lib/${ARCH}-linux-gnu/libpq.so.* \
       /usr/lib/${ARCH}-linux-gnu/liblber.so.* \
       /usr/lib/${ARCH}-linux-gnu/libldap.so.* \
       /usr/lib/${ARCH}-linux-gnu/libsasl2.so.* \
       /usr/lib/linux-gnu/

COPY pyproject.toml uv.lock ./

RUN uvx pip wheel --wheel-dir /build/wheels .


FROM ${BASE_REGISTRY}/python:3.13-slim-trixie AS app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY --from=build-image /build/wheels /wheels
COPY --from=build-image /usr/lib/linux-gnu/* /usr/lib/linux-gnu/

RUN if [ -z "$ARCH" ]; then ARCH="$(uname -m)"; fi && \
    cp /usr/lib/linux-gnu/* /usr/lib/${ARCH}-linux-gnu/ && \
    rm -rf /usr/lib/linux-gnu && \
    python3 -m pip install --no-cache-dir --no-index --no-deps /wheels/* && \
    rm -rf /wheels && \
    apt clean && \
    groupadd -r appgroup && \
    useradd -r -G appgroup -d /app appuser && \
    install -d -o appuser -g appgroup /app

WORKDIR /app
USER appuser

COPY --chown=appuser src/fastapi_project_template ./fastapi_project_template/
COPY --chown=appuser migrations ./migrations/
COPY --chown=appuser alembic.ini ./alembic.ini

EXPOSE 8000

CMD ["python3", "-m", "fastapi_project_template"]
