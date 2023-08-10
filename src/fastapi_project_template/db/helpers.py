import logging

import sqlalchemy as sa
from fastapi_users.exceptions import UserAlreadyExists
from passlib import pwd
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.api.v1.schemas import UserCreate
from fastapi_project_template.conf import settings
from fastapi_project_template.core.users import create_user
from fastapi_project_template.db.models import User

logger = logging.getLogger()


async def bootstrap_db(session: AsyncSession):
    cursor = await session.execute(sa.select(sa.func.count(User.id)))
    user_count = cursor.scalar_one()

    if user_count == 0:
        logger.warning('No users in database')

        if settings.bootstrap_user_email:
            logger.info('Bootstrapping a user in database')
            password = pwd.genword(length=16, entropy=52)

            try:
                await create_user(
                    UserCreate(
                        email=settings.bootstrap_user_email,
                        password=password,
                        is_superuser=True,
                        is_active=True,
                        is_verified=True
                    )
                )
                logger.debug(f'Bootstrap user: {settings.bootstrap_user_email} / {password}')
            except UserAlreadyExists:
                logger.warning(f'User {settings.bootstrap_user_email} already exist')
