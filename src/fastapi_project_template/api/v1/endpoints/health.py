import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.api.v1.routers import health_router
from fastapi_project_template.db import get_main_db_session

logger = logging.getLogger(__name__)
AsyncSessionDep = Annotated[AsyncSession, Depends(get_main_db_session)]


@health_router.get('/alive')
async def alive() -> bool:
    return True


@health_router.get('/ready')
async def ready(session: AsyncSessionDep) -> None:
    query = text('SELECT 1;')

    try:
        result = await session.execute(query)
        value = result.scalar_one()
    except Exception:
        logger.exception('Failed readiness check for database.')
        value = None

    if value != 1:
        raise HTTPException(status_code=503)
