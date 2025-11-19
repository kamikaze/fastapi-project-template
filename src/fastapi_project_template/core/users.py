from __future__ import annotations

import contextlib
import logging
import uuid
from typing import TYPE_CHECKING, Annotated

import msgspec
import sqlalchemy as sa
from fastapi import Depends, Request
from fastapi_commons.db.models import User
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.password import PasswordHelper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from passlib.context import CryptContext
from python3_commons.db.models import UserGroup

from fastapi_project_template.api.v1.schemas import UserApiSchema, UserCreate, UserUpdate
from fastapi_project_template.conf import settings
from fastapi_project_template.db.user_db_helpers import get_user_db, get_user_db_context

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.sql.selectable import Select

logger = logging.getLogger(__name__)
context = CryptContext(schemes=['argon2', 'bcrypt'], deprecated='auto')
password_helper = PasswordHelper(context)
UserDbDep = Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]


class UserGroupItem(msgspec.Struct):
    id: int
    name: str


class UserManager(UUIDIDMixin, BaseUserManager[UserApiSchema, uuid.UUID]):
    reset_password_token_secret = settings.auth_secret.get_secret_value()
    verification_token_secret = settings.auth_secret.get_secret_value()

    async def on_after_register(self, user: UserApiSchema, request: Request | None = None) -> None:
        msg = f'User {user.id} has registered.'
        logger.info(msg)

        await super().on_after_register(user, request)

    async def on_after_forgot_password(self, user: UserApiSchema, token: str, request: Request | None = None) -> None:
        msg = f'User {user.id} has forgot their password. Reset token: {token}'
        logger.info(msg)

        await super().on_after_forgot_password(user, token, request)

    async def on_after_request_verify(self, user: UserApiSchema, token: str, request: Request | None = None) -> None:
        msg = f'Verification requested for user {user.id}. Verification token: {token}'
        logger.info(msg)

        await super().on_after_request_verify(user, token, request)


async def get_user_manager(user_db: UserDbDep) -> AsyncGenerator[UserManager]:
    yield UserManager(user_db, password_helper)


get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(user: UserCreate) -> None:
    async with get_user_db_context() as user_db, get_user_manager_context(user_db) as user_manager:
        await user_manager.create(user)


async def update_user(user_id: str, user: UserUpdate) -> UserUpdate:
    user.id = user_id

    async with get_user_db_context() as user_db, get_user_manager_context(user_db) as user_manager:
        r = await user_manager.update(user)

        msg = f'updated: {r}'
        logger.info(msg)

    return user


def get_users_stmt() -> Select:
    return sa.select(User)


async def get_user(session: AsyncSession, user_id: str) -> User:
    stmt = sa.select(User).where(User.id == user_id)
    cursor = await session.execute(stmt)

    return cursor.scalar_one()


async def get_user_groups_stmt() -> Select[tuple[UserGroup, ...]]:
    return sa.select(UserGroup).order_by(UserGroup.name)
