import logging
import uuid
from functools import wraps
from inspect import signature
from typing import Sequence

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import ORJSONResponse
from fastapi_pagination import Page
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, CookieTransport
from pydantic import Json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template import core
from fastapi_project_template.api.v1.schemas import (
    UserCreate, UserUpdate, UserItem, UserGroup, UserRead
)
from fastapi_project_template.conf import settings
from fastapi_project_template.core import users
from fastapi_project_template.core.users import get_user_manager
from fastapi_project_template.db.models import User
from fastapi_project_template.db.user_db_helpers import get_async_session

logger = logging.getLogger(__name__)
router = APIRouter()
cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.auth_secret.get_secret_value(), lifetime_seconds=3600)


auth_backend = AuthenticationBackend(name='userauth', transport=cookie_transport, get_strategy=get_jwt_strategy)
auth_backends = [auth_backend, ]
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    auth_backends
)
get_current_user = fastapi_users.current_user(active=True)
auth_router = fastapi_users.get_auth_router(auth_backend, requires_verification=True)
users_router = fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True)


def _handle_exceptions_helper(status_code, *args):
    if args:
        raise HTTPException(status_code=status_code, detail=args[0])
    else:
        raise HTTPException(status_code=status_code)


def handle_exceptions(func):
    signature(func)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except PermissionError as e:
            return _handle_exceptions_helper(status.HTTP_401_UNAUTHORIZED, *e.args)
        except LookupError as e:
            return _handle_exceptions_helper(status.HTTP_404_NOT_FOUND, *e.args)
        except ValueError as e:
            return _handle_exceptions_helper(status.HTTP_400_BAD_REQUEST, *e.args)

    return wrapper


@router.get('/users', response_class=ORJSONResponse, tags=['Admin'])
@handle_exceptions
async def get_users(search: Json | None = None, order_by: str | None = None,
                    user=Depends(get_current_user),
                    session: AsyncSession = Depends(get_async_session)) -> Page[UserItem]:
    if user.is_superuser:
        return await core.get_users(session, search, order_by)

    raise HTTPException(status_code=403)


@router.post('/users', response_class=ORJSONResponse, tags=['Admin'])
@handle_exceptions
async def create_user(new_user: UserCreate, user=Depends(get_current_user)) -> UserItem:
    if user.is_superuser:
        created_user = await users.create_user(new_user)

        return created_user

    raise HTTPException(status_code=403)


@router.get('/user-groups', response_class=ORJSONResponse, tags=['Admin'])
@handle_exceptions
async def get_user_groups(search: Json | None = None, order_by: str | None = None,
                          user=Depends(get_current_user),
                          session: AsyncSession = Depends(get_async_session)) -> Sequence[UserGroup]:
    if user.is_active:
        return await core.get_user_groups(session, search, order_by)

    raise HTTPException(status_code=403)


@router.get('/alive', tags=['Probes'])
async def alive():
    return


@router.get('/ready', tags=['Probes'])
async def ready(session: AsyncSession = Depends(get_async_session)):
    query = text('SELECT 1;')

    cursor = await session.execute(query)
    value = cursor.scalar_one()

    if value != 1:
        raise HTTPException(status_code=503)
