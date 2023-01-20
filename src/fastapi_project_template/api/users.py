import contextlib
import logging
import uuid

from fastapi import Request, Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from fastapi_project_template.api.v1.schemas import UserCreate, UserUpdate
from fastapi_project_template.conf import settings
from fastapi_project_template.db.models import User
from fastapi_project_template.db.user_db_helpers import get_user_db, get_user_db_context

logger = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.auth_secret.get_secret_value()
    verification_token_secret = settings.auth_secret.get_secret_value()

    async def on_after_register(self, user: User, request: Request | None = None):
        logger.info(f'User {user.id} has registered.')

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None):
        logger.info(f'User {user.id} has forgot their password. Reset token: {token}')

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None):
        logger.info(f'Verification requested for user {user.id}. Verification token: {token}')


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(user: UserCreate):
    async with get_user_db_context() as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            await user_manager.create(user)


async def update_user(user_id: str, user: UserUpdate):
    user.id = user_id

    async with get_user_db_context() as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            r = await user_manager.update(user)

            logger.info(f'updated: {r}')

    return user
