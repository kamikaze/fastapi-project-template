import logging
import uuid
from functools import wraps
from inspect import signature
from typing import Optional, Any, List

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import ORJSONResponse
from fastapi_pagination import Page
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, CookieTransport
from pydantic import Json

from fastapi_project_template import core
from fastapi_project_template.api import users
from fastapi_project_template.api.users import get_user_manager
from fastapi_project_template.api.v1.schemas import (
    UserCreate, UserUpdate, UserItem, UserGroup, UserRead
)
from fastapi_project_template.conf import settings
from fastapi_project_template.db import database
from fastapi_project_template.db.models import User
from fastapi_project_template.helpers import connect_to_db

logger = logging.getLogger(__name__)
router = APIRouter()
cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.auth_secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(name='cluserauth', transport=cookie_transport, get_strategy=get_jwt_strategy)
auth_backends = [auth_backend, ]
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    auth_backends
)
get_current_user = fastapi_users.current_user(active=True)
auth_router = fastapi_users.get_auth_router(auth_backend, requires_verification=True)
users_router = fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True)


@router.on_event('startup')
async def startup():
    await connect_to_db(database)


@router.on_event('shutdown')
async def shutdown():
    await database.disconnect()


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


@router.get('/users', response_model=Page[UserItem], response_class=ORJSONResponse, tags=['Admin'])
@handle_exceptions
async def get_users(search: Optional[Json] = None, order_by: Optional[str] = None,
                    user=Depends(get_current_user)):
    if user.is_superuser:
        return await core.get_users(database, search, order_by)

    raise HTTPException(status_code=403)


@router.post('/users', response_model=UserItem, response_class=ORJSONResponse, tags=['Admin'])
@handle_exceptions
async def create_user(new_user: UserCreate, user=Depends(get_current_user)):
    if user.is_superuser:
        created_user = await users.create_user(new_user)

        return created_user

    raise HTTPException(status_code=403)


@router.get('/user-groups', response_model=List[UserGroup], response_class=ORJSONResponse, tags=['Admin'])
@handle_exceptions
async def get_user_groups(search: Optional[Json[Any]] = None, order_by: Optional[str] = None,
                          user=Depends(get_current_user)):
    if user.is_active:
        return await core.get_user_groups(database, search, order_by)

    raise HTTPException(status_code=403)
