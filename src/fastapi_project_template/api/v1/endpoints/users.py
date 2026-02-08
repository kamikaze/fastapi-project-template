import logging
from collections.abc import Mapping
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_commons.auth import get_token_verifier
from python3_commons.auth import TokenData
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.db import get_main_db_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/users', tags=['Users'])
AsyncSessionDep = Annotated[AsyncSession, Depends(get_main_db_session)]
JWKS = {}
get_verified_token = get_token_verifier(TokenData, JWKS)


@router.get('/me')
async def get_current_user_profile(_: Annotated[TokenData, Depends(get_verified_token)]) -> Mapping:
    return {
        'email': 'me@project.eu',
    }
