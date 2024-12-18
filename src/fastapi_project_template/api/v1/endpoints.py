import logging
from typing import Sequence

from fastapi import HTTPException, Depends
from fastapi_pagination import Page
from pydantic import Json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template import core
from fastapi_project_template.api.v1.auth import get_current_user
from fastapi_project_template.api.v1.handlers import handle_exceptions
from fastapi_project_template.api.v1.routers import router
from fastapi_project_template.api.v1.schemas import UserCreate, UserItem, UserGroup
from fastapi_project_template.core import users
from fastapi_project_template.db.user_db_helpers import get_async_session

logger = logging.getLogger(__name__)


@router.get('/users', tags=['Admin'])
@handle_exceptions
async def get_users(search: Json | None = None, order_by: str | None = None,
                    user=Depends(get_current_user),
                    session: AsyncSession = Depends(get_async_session)) -> Page[UserItem]:
    if user.is_superuser:
        return await core.get_users(session, search, order_by)

    raise HTTPException(status_code=403)


@router.post('/users', tags=['Admin'])
@handle_exceptions
async def create_user(new_user: UserCreate, user=Depends(get_current_user)) -> UserItem:
    if user.is_superuser:
        created_user = await users.create_user(new_user)

        return created_user

    raise HTTPException(status_code=403)


@router.get('/user-groups', tags=['Admin'])
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
