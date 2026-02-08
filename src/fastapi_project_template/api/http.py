import logging.config
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from uuid import uuid4

import starlette.middleware.base
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from fastapi_project_template import ctx_correlation_id
from fastapi_project_template.api.v1.endpoints import config, health
from fastapi_project_template.conf import settings

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {'format': settings.logging_format},
        'json': {
            '()': 'python3_commons.log.formatters.JSONFormatter',
        },
    },
    'filters': {'info_and_below': {'()': 'python3_commons.log.filters.filter_maker', 'level': 'INFO'}},
    'handlers': {
        'default_stdout': {
            'level': settings.logging_level,
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': settings.logging_formatter,
            'filters': [
                'info_and_below',
            ],
        },
        'default_stderr': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': settings.logging_formatter,
        },
    },
    'loggers': {
        '': {
            'handlers': [
                'default_stderr',
                'default_stdout',
            ],
        },
        'fastapi_project_template': {
            'handlers': [
                'default_stderr',
                'default_stdout',
            ],
            'level': settings.logging_level,
            'propagate': False,
        },
        '__main__': {
            'handlers': [
                'default_stderr',
                'default_stdout',
            ],
            'level': settings.logging_level,
            'propagate': False,
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)
origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:3000',
]


class CorrelationIdMiddleware(starlette.middleware.base.BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: starlette.middleware.base.RequestResponseEndpoint
    ) -> Response:
        correlation_id = str(uuid4())
        ctx_correlation_id.set(correlation_id)

        return await call_next(request)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    yield


app_prefix = '/api/project'
app = FastAPI(
    default_response_class=ORJSONResponse,
    docs_url=f'{app_prefix}/docs',
    openapi_url=f'{app_prefix}/v1/openapi.json',
    lifespan=lifespan,
    title='Project backend',
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health.router, prefix=f'{app_prefix}/v1')
app.include_router(config.router, prefix=f'{app_prefix}/v1')

add_pagination(app)
