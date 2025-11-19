import logging

from fastapi_users.exceptions import UserAlreadyExists

from fastapi_project_template.api.v1.schemas import UserCreate
from fastapi_project_template.conf import settings
from fastapi_project_template.core.users import get_user_manager_context
from fastapi_project_template.db import async_session_manager
from fastapi_project_template.db.user_db_helpers import get_user_db_context

logger = logging.getLogger(__name__)


async def create_superuser() -> None:
    try:
        if not settings.bootstrap_user_name:
            msg = 'No name is set for a bootstrapped user.'

            raise ValueError(msg)

        if not settings.bootstrap_user_password:
            msg = 'No password is set for a bootstrapped user.'

            raise ValueError(msg)

        async_session_context = async_session_manager.get_session_context('main')

        async with (
            async_session_context() as session,
            get_user_db_context(session) as user_db,
            get_user_manager_context(user_db) as user_manager,
        ):
            await user_manager.create(
                UserCreate(
                    username=settings.bootstrap_user_name,
                    email=settings.bootstrap_user_email,
                    password=settings.bootstrap_user_password.get_secret_value(),
                    is_superuser=True,
                    is_active=True,
                    is_verified=True,
                )
            )
            msg = f'User created: {settings.bootstrap_user_email}'

            logger.info(msg)
    except UserAlreadyExists:
        msg = f'User already exists: {settings.bootstrap_user_email}'

        logger.info(msg)
