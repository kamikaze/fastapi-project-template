import contextlib
import logging
import uuid
from collections.abc import AsyncGenerator, Mapping, Sequence
from typing import Annotated

import sqlalchemy as sa
from fastapi import Depends, Request
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.password import PasswordHelper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from passlib.context import CryptContext
from python3_commons.db.models import User, UserGroup
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.api.v1.schemas import UserCreate, UserGroupItem, UserItem, UserUpdate
from fastapi_project_template.conf import settings
from fastapi_project_template.db.user_db_helpers import get_user_db, get_user_db_context

logger = logging.getLogger(__name__)
UserDBDep = Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]
context = CryptContext(schemes=['argon2', 'bcrypt'], deprecated='auto')
password_helper = PasswordHelper(context)


class UserManager(UUIDIDMixin, BaseUserManager[UserItem, uuid.UUID]):
    reset_password_token_secret = settings.auth_secret.get_secret_value()
    verification_token_secret = settings.auth_secret.get_secret_value()

    async def on_after_register(self, user: UserItem, request: Request | None = None) -> None:
        logger.info(f'User {user.id} has registered.')

    async def on_after_forgot_password(self, user: UserItem, token: str, request: Request | None = None) -> None:
        logger.info(f'User {user.id} has forgot their password. Reset token: {token}')

    async def on_after_request_verify(self, user: UserItem, token: str, request: Request | None = None) -> None:
        logger.info(f'Verification requested for user {user.id}. Verification token: {token}')


async def get_user_manager(user_db: UserDBDep) -> AsyncGenerator[UserManager]:
    yield UserManager(user_db, password_helper)


get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(user: UserCreate) -> None:
    async with get_user_db_context() as user_db, get_user_manager_context(user_db) as user_manager:
        await user_manager.create(user)


async def update_user(user_id: str, user: UserUpdate) -> UserUpdate:
    user.id = user_id

    async with get_user_db_context() as user_db, get_user_manager_context(user_db) as user_manager:
        r = await user_manager.update(user)

        logger.info(f'updated: {r}')

    return user


async def get_users(
    session: AsyncSession, search: Mapping[str, str] | None = None, order_by: str | None = None
) -> Page[UserItem]:
    query = sa.select(User)

    return await apaginate(session, query)


async def get_user(session: AsyncSession, user_id: str) -> User:
    query = sa.select(User).where(User.id == user_id)
    cursor = await session.execute(query)

    return cursor.scalar_one()


async def get_user_groups(
    session: AsyncSession, search: Mapping[str, str] | None = None, order_by: str | None = None
) -> Sequence[UserGroupItem]:
    query = sa.select(UserGroup).order_by(UserGroup.name)
    cursor = await session.execute(query)

    return cursor.scalars()
