import logging.config
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
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


app_prefix = '/api/app'
app = FastAPI(
    default_response_class=ORJSONResponse,
    docs_url=f'{app_prefix}/docs',
    openapi_url=f'{app_prefix}/openapi.json',
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

root_router = APIRouter(prefix=f'{app_prefix}/v1')
root_router.include_router(health.router)
root_router.include_router(config.router)
root_router.include_router(users.router)
app.include_router(root_router)

add_pagination(app)
