import logging.config
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi_commons.middleware.correlation_id import CorrelationIDMiddleware
from fastapi_commons.middleware.log_context import LogContextMiddleware
from fastapi_pagination import add_pagination
from scalar_fastapi import AgentScalarConfig, get_scalar_api_reference
from starlette.applications import Starlette

from fastapi_project_template.api.v1.endpoints import config, health, users
from fastapi_project_template.conf import LOGGING_CONFIG, settings

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: Starlette) -> AsyncGenerator:
    msg = f'Starting backend API service at: {settings.service_addr}:{settings.service_port}'
    logger.info(msg)

    yield

    logger.info('Shutting down backend API service.')


api_prefix = '/api/app'
app = FastAPI(
    openapi_url=f'{api_prefix}/openapi.json',
    lifespan=lifespan,
    version='1.0.0',
    title='App backend',
    description='Backend API service.',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(LogContextMiddleware)

root_router = APIRouter(prefix=f'{api_prefix}/v1')
root_router.include_router(health.router)
root_router.include_router(config.router)
root_router.include_router(users.router)
app.include_router(root_router)

add_pagination(app)


@app.get(f'{api_prefix}/docs', include_in_schema=False)
async def scalar_html() -> HTMLResponse:
    return get_scalar_api_reference(
        agent=AgentScalarConfig(disabled=True),
        openapi_url=app.openapi_url,
    )
