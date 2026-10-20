# FastAPI Project Template

An idiomatic FastAPI project template with C and Rust extension modules built into the same package.

## Features

- **FastAPI** on Python 3.15, served by [Granian](https://github.com/emmett-framework/granian).
- **Native extensions**: one `_ext` module that contains C and Rust code, built with [maturin](https://www.maturin.rs/).
- **Shared building blocks** from [`python3-commons`](https://github.com/kamikaze/python3-commons) (settings, async DB sessions, base models, JSON logging) and [`fastapi-commons`](https://github.com/kamikaze/fastapi-commons) (OIDC token verification, API key auth settings, correlation ID and log context middleware, exception handlers).
- **Database**: async SQLAlchemy over `asyncpg`, with Alembic migrations and a separate read-only connection.
- **Auth**: OIDC bearer tokens ([Dex](https://dexidp.io/) in the dev stack) or `Api-Key` header, with authorization through [Open Policy Agent](https://www.openpolicyagent.org/).
- **API reference** UI by [Scalar](https://github.com/scalar/scalar), plus pagination through `fastapi-pagination`.
- **Tooling**: `uv`, `ruff`, `pyright`, `pytest` and `pre-commit`.
- **Deployment**: a hardened `Containerfile`, a Compose dev stack and a Helm chart.

## Project structure

| Path | Contents |
| --- | --- |
| `src/fastapi_project_template/` | Application code: `api/` (HTTP layer), `core/`, `services/`, `db/models/`, `jobs/`, `conf.py` |
| `rustlib/` | Rust extension source |
| `clib/` | C extension source |
| `Cargo.toml`, `build.rs` | Native extension build configuration |
| `migrations/` | Alembic migrations |
| `tests/` | Unit tests |
| `compose.yml` | Local stack: PostgreSQL, Dex, OPA, MinIO, RabbitMQ, Valkey, frontend and backend |
| `.helm/` | Helm chart |

## Prerequisites

- Python 3.15
- Rust toolchain and a C compiler, to build the extensions
- [`uv`](https://docs.astral.sh/uv/)

## Getting started

1. Clone the repository:

   ```bash
   git clone https://github.com/kamikaze/fastapi-project-template.git
   cd fastapi-project-template
   ```

2. Install dependencies. `uv sync` builds the project through maturin, so the native extensions are compiled and installed at the same time:

   ```bash
   uv sync --all-groups
   ```

3. Create a local configuration and start the services the app needs. The app does not load `.env` by itself; the commands below pass it with `uv run --env-file`:

   ```bash
   cp .env_template .env
   podman compose up -d db dex opa valkey   # or: docker compose
   ```

4. Apply database migrations:

   ```bash
   uv run --env-file .env alembic upgrade head
   ```

5. Run the API server (listens on `0.0.0.0:8080` by default):

   ```bash
   uv run --env-file .env python -m fastapi_project_template
   ```

   The API reference is at <http://localhost:8080/api/app/docs> and the OpenAPI schema is at `/api/app/openapi.json`.

To run the full stack, including the backend container, use `podman compose up --build`. The backend is then published on port `8000`.

### Local OIDC provider

The compose stack runs [Dex](https://dexidp.io/) at <http://localhost:5556/dex>, configured in `.docker/dex/config.yaml`. It has a public `frontend` client and two users, both with the password `dev`:

| User | Groups |
| --- | --- |
| `admin@example.com` | `admin`, `view-profile` |
| `user@example.com` | `view-profile` |

The backend reads roles from the token's `groups` claim (requested with the `groups` scope), as well as from Keycloak's `realm_access` and `resource_access` claims, and sends them to OPA. Dex keeps its state in memory, so sessions are lost when the container restarts.

## Configuration

Settings are read from environment variables:

| Variable | Purpose |
| --- | --- |
| `DB_DSN`, or `DB_HOST` / `DB_PORT` / `DB_NAME` / `DB_USER` / `DB_PASS` | Main database |
| `RO_DB_DSN` | Read-only database. Falls back to the main database when unset |
| `SERVICE_ADDR`, `SERVICE_PORT` | Bind address and port |
| `ALLOWED_ORIGINS` | Comma-separated list of CORS origins |
| `LOGGING_LEVEL`, `LOGGING_FORMATTER` | Log level, and `default` or `json` output |
| `VALKEY_DSN`, `VALKEY_SENTINEL_DSN` | Valkey connection |
| `API_AUTH_ENABLED` | Require authentication on the API |
| `OIDC_AUTHORITY_URL` | OIDC issuer URL as the browser sees it |
| `OIDC_AUTHORITY_INTERNAL_HOST` | Origin that replaces the issuer's origin for server-side calls, for example `http://dex:5556/` inside compose |
| `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `OIDC_REDIRECT_URI` | OIDC client |
| `OIDC_AUDIENCE` | Expected `aud` claim. Must be set when tokens carry an audience |
| `OIDC_SCOPE` | Comma-separated scopes, for example `openid,profile,email,groups` |
| `OPA_URL` | OPA decision endpoint used for authorization |
| `OBJECT_STORAGE_WORK_PATH`, `S3_*` | Object storage root (for example `s3://bucket`) and S3 credentials |

See `src/fastapi_project_template/conf.py` and the settings classes in `python3_commons.conf` and `fastapi_commons.conf` for the full list.

## API

All endpoints are under `/api/app/v1`:

| Method and path | Description |
| --- | --- |
| `GET /alive`, `GET /ready` | Liveness and readiness probes. Readiness checks the database |
| `GET /config` | Public client configuration (OIDC settings for the frontend) |
| `GET /users/me`, `GET /users`, `POST /users/{uid}` | User endpoints, authorized through OPA |
| `POST /extensions/fibonacci` | Demo of the native extensions |

## Native extensions

The `_ext` module exposes a C function and a Rust function, both re-exported from `fastapi_project_template`:

- `c_fib(n)`: Fibonacci number, implemented in C.
- `rust_fib(n)`: Fibonacci number, implemented in Rust.

```bash
curl -X POST http://localhost:8080/api/app/v1/extensions/fibonacci \
     -H "Content-Type: application/json" \
     -d '{"n": 10}'
```

## Background jobs

Jobs run as one-off processes, for example as the Kubernetes CronJobs defined in the Helm chart:

```bash
uv run --env-file .env python -m fastapi_project_template.jobs --job poc
```

## Development

Run the tests:

```bash
uv run pytest tests/unit/
```

Lint, format and type-check:

```bash
uv run ruff format ./src/ ./tests/
uv run ruff check --extend-select I ./src/ ./tests/
uv run pyright ./src/ ./tests/
```

Create a migration after you change the models:

```bash
uv run --env-file .env alembic revision --autogenerate -m "describe the change"
```

Build a release wheel or a container image:

```bash
uvx maturin build --release
podman build -t fastapi-project-template -f Containerfile .
```

## License

GPL-3.0. See [LICENSE](LICENSE).
