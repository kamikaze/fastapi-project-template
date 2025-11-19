import contextlib
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi_commons.db.models import User
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.db import get_main_db_session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_main_db_session)]


async def get_user_db(db_session: AsyncSessionDep) -> AsyncGenerator[SQLAlchemyUserDatabase]:
    yield SQLAlchemyUserDatabase(db_session, User)


get_user_db_context = contextlib.asynccontextmanager(get_user_db)
