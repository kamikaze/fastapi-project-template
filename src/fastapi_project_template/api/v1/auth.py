import logging
import uuid
from collections.abc import Callable, Coroutine
from http import HTTPStatus
from typing import Annotated, Any

import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from fastapi_commons.auth import get_token_verifier
from fastapi_commons.exceptions import UnauthorizedError
from python3_commons.auth import TokenData
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi_project_template.conf import settings
from fastapi_project_template.db import get_main_db_session
from fastapi_project_template.db.models import ApiKey

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)
optional_api_key_header = APIKeyHeader(name='Api-Key', auto_error=False)


class AppTokenData(TokenData):
    """
    Token claims including the ``groups`` claim, which Dex and most other OIDC providers use instead of
    Keycloak's ``realm_access`` and ``resource_access``.
    """

    @property
    def roles(self) -> list[str]:
        return list({*super().roles, *self.groups})


async def _no_token() -> None:
    return None


# Decided once at import: with authentication disabled every verified-token dependency yields None.
get_verified_token: Callable[..., Coroutine[Any, Any, AppTokenData | None]] = (
    get_token_verifier(AppTokenData) if settings.api_auth_enabled else _no_token
)


async def get_current_token(token: Annotated[AppTokenData | None, Depends(get_verified_token)]) -> AppTokenData:
    """Return the verified token, or answer 401 when authentication is disabled and there is no identity."""
    if token is None:
        msg = 'Not authenticated'
        raise UnauthorizedError(msg, headers={'WWW-Authenticate': 'Bearer'})

    return token


AsyncSessionDep = Annotated[AsyncSession, Depends(get_main_db_session)]


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
    api_key_value: Annotated[uuid.UUID, Depends(optional_api_key_header)] | None,
    token_data: Annotated[AppTokenData, Depends(get_verified_token)] | None,
    db_session: AsyncSessionDep,
) -> ApiKey | AppTokenData | None:
    if settings.api_auth_enabled:
        if api_key_value:
            api_key = await verify_api_key(api_key_value, db_session)
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
