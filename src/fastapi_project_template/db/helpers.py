import logging

import sqlalchemy as sa
from fastapi_users.manager import UserAlreadyExists
from passlib import pwd

from fastapi_project_template.api.users import create_user
from fastapi_project_template.api.v1.models import UserCreate
from fastapi_project_template.conf import settings
from fastapi_project_template.db import database
from fastapi_project_template.db.models import UserTable

logger = logging.getLogger()


async def bootstrap_db():
    user_count = await database.fetch_val(sa.select([sa.func.count(UserTable.id)]))

    if user_count == 0:
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
