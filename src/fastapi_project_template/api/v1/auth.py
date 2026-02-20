import logging
import uuid
from http import HTTPStatus
from typing import Annotated, TypeVar

import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader, HTTPBearer
from fastapi_commons.auth import get_token_verifier
from fastapi_commons.conf import api_auth_settings
from python3_commons.auth import TokenData
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi_project_template.db import get_main_db_session
from fastapi_project_template.db.models import ApiKey

logger = logging.getLogger(__name__)

_JWKS = {}

api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)
optional_api_key_header = APIKeyHeader(name='X-API-Key', auto_error=False)
bearer_security = HTTPBearer(auto_error=api_auth_settings.enabled)
optional_bearer_security = HTTPBearer(auto_error=False)


get_verified_token = get_token_verifier(TokenData, _JWKS)

AsyncSessionDep = Annotated[AsyncSession, Depends(get_main_db_session)]
T = TypeVar('T', bound=TokenData)


async def verify_api_key(api_key: Annotated[uuid.UUID, Depends(api_key_header)], session: AsyncSessionDep) -> ApiKey:
    stmt = sa.select(ApiKey).where(ApiKey.uid == api_key)
    result = await session.execute(stmt)
    row = result.fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid service API Key',
            headers={'WWW-Authenticate': 'APIKey'},
        )

    return row[0]


async def get_auth(
    api_key: Annotated[uuid.UUID, Depends(optional_api_key_header)] | None,
    token_data: Annotated[TokenData, Depends(get_verified_token)] | None,
    db_session: AsyncSessionDep,
) -> ApiKey | TokenData | None:
    if api_auth_settings.enabled:
        if api_key:
            api_key = await verify_api_key(api_key, db_session)
            msg = f'Authenticated API key: id={api_key.uid}, name={api_key.name}'
            logger.debug(msg)

            return api_key

        if token_data:
            return token_data

        msg = 'Invalid authentication credentials'

        logger.warning(msg)

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=msg,
        )

    return None
