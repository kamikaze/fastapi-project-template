import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.db import get_main_db_session

logger = logging.getLogger(__name__)
router = APIRouter(tags=['health'])
AsyncSessionDep = Annotated[AsyncSession, Depends(get_main_db_session)]


@router.get('/alive')
async def alive() -> bool:
    return True


@router.get('/ready')
async def ready(db_session: AsyncSessionDep) -> None:
    query = text('SELECT 1;')

    try:
        result = await db_session.execute(query)
        value = result.scalar_one()
    except Exception:
        logger.exception('Failed readiness check for database.')
        value = None

    if value != 1:
        raise HTTPException(status_code=503)
