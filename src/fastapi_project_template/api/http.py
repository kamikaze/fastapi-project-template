import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from starlette.applications import Starlette

from fastapi_project_template.api.v1.endpoints import router
from fastapi_project_template.api.v1.routers import auth_router, users_router
from fastapi_project_template.conf import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: Starlette):
    logger.info('Started an application.')
    yield


app = FastAPI(default_response_class=ORJSONResponse, docs_url='/api/docs', openapi_url='/api/v1/openapi.json',
              lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(router, prefix='/api/v1')
app.include_router(
    auth_router,
    prefix='/api/v1/auth',
    tags=['auth'],
)
app.include_router(
    users_router,
    prefix='/api/v1/users',
    tags=['users'],
)
add_pagination(app)
