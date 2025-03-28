import logging

from fastapi import HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.api.v1.routers import health_router
from fastapi_project_template.db import get_main_db_session

logger = logging.getLogger(__name__)


@health_router.get('/alive')
async def alive() -> bool:
    return True


@health_router.get('/ready')
async def ready(session: AsyncSession = Depends(get_main_db_session)):
    query = text('SELECT 1;')

    try:
        result = await session.execute(query)
        value = result.scalar_one()
    except Exception as e:
        logger.error(f'Failed readiness check for database: {e}')
        value = None

    if value != 1:
        raise HTTPException(status_code=503)
