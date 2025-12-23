ARG BASE_REGISTRY=docker.io/library
FROM ${BASE_REGISTRY}/python:3.14.2-slim-trixie AS build-image

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.cargo/bin:${PATH}"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /build

RUN if [ -z "$ARCH" ]; then ARCH="$(uname -m)"; fi && \
    apt update && \
    apt upgrade -y && \
    apt install -y curl ca-certificates gnupg2 && \
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql.gpg && \
    echo deb [arch=amd64,arm64,ppc64el signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt/ trixie-pgdg main | tee /etc/apt/sources.list.d/postgresql.list && \
    apt update && \
    apt install -y --no-install-recommends gcc g++ make cmake postgresql-server-dev-18 libpq-dev libpq5 libffi-dev git pkg-config nfs-common && \
    curl https://sh.rustup.rs -sSf | bash -s -- -y && \
    mkdir -p /usr/lib/linux-gnu && \
    cp /usr/lib/${ARCH}-linux-gnu/libpq.so.* \
       /usr/lib/${ARCH}-linux-gnu/liblber.so.* \
       /usr/lib/${ARCH}-linux-gnu/libldap.so.* \
       /usr/lib/${ARCH}-linux-gnu/libsasl2.so.* \
       /usr/lib/${ARCH}-linux-gnu/libgobject-2.0.so.* \
       /usr/lib/linux-gnu/ && \
    mkdir -p /lib/linux-gnu && \
    cp /lib/${ARCH}-linux-gnu/libtirpc.so.* \
    /lib/${ARCH}-linux-gnu/libnfsidmap.so.* \
    /lib/${ARCH}-linux-gnu/libgssapi_krb5.so.* \
    /lib/${ARCH}-linux-gnu/libkrb5.so.* \
    /lib/${ARCH}-linux-gnu/libk5crypto.so.* \
    /lib/${ARCH}-linux-gnu/libcom_err.so.* \
    /lib/${ARCH}-linux-gnu/libkrb5support.so.* \
    /lib/linux-gnu/

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --frozen --no-install-project && \
    find .venv/lib/python3.14/site-packages -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find .venv/lib/python3.14/site-packages -type f -name "*.pyc" -delete && \
    find .venv/lib/python3.14/site-packages -type f -name "*.pyo" -delete && \
    find .venv/lib/python3.14/site-packages -name "*.so" -exec strip {} \; 2>/dev/null || true && \
    cp -r .venv/lib/python3.14/site-packages /install-packages


FROM ${BASE_REGISTRY}/python:3.14.2-slim-trixie AS app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=build-image /install-packages /usr/local/lib/python3.14/site-packages/
COPY --from=build-image /lib/linux-gnu/* /lib/linux-gnu/
COPY --from=build-image /usr/lib/linux-gnu/* /usr/lib/linux-gnu/

WORKDIR /app

RUN if [ -z "$ARCH" ]; then ARCH="$(uname -m)"; fi && \
    apt clean && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/ && \
    cp /lib/linux-gnu/* /lib/${ARCH}-linux-gnu/ && \
    cp /usr/lib/linux-gnu/* /usr/lib/${ARCH}-linux-gnu/ && \
    rm -rf /lib/linux-gnu /usr/lib/linux-gnu && \
    groupadd -r appgroup && \
    useradd -r -G appgroup -d /app appuser && \
    install -d -o appuser -g appgroup /app && \
    chown -Rc appuser:appgroup /app

USER  appuser
COPY --chown=appuser src/fastapi_project_template ./fastapi_project_template/
COPY --chown=appuser migrations ./migrations/
COPY --chown=appuser alembic.ini ./alembic.ini
EXPOSE 8000

ENTRYPOINT ["python3", "-m", "fastapi_project_template"]
