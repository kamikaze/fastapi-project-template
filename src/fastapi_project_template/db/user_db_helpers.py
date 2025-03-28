import contextlib

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from python3_commons.db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.db import async_session_manager


async def get_user_db(session: AsyncSession = Depends(async_session_manager.get_async_session('main'))):
    yield SQLAlchemyUserDatabase(session, User)


get_user_db_context = contextlib.asynccontextmanager(get_user_db)
