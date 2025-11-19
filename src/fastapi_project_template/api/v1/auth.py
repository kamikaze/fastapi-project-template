import logging
import uuid
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from fastapi_commons.db.models import ApiKey, User
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi_project_template.conf import settings
from fastapi_project_template.core.users import get_user_manager
from fastapi_project_template.db import get_main_db_session

logger = logging.getLogger(__name__)
AsyncSessionDep = Annotated[AsyncSession, Depends(get_main_db_session)]
cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.auth_secret.get_secret_value(), lifetime_seconds=3600)


auth_backend = AuthenticationBackend(name='cluserauth', transport=cookie_transport, get_strategy=get_jwt_strategy)
auth_backends = [
    auth_backend,
]
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, auth_backends)
get_current_user = fastapi_users.current_user(active=True)
get_current_superuser = fastapi_users.current_user(active=True, superuser=True)
optional_get_current_user = fastapi_users.current_user(optional=True, active=True)
optional_get_current_superuser = fastapi_users.current_user(optional=True, active=True, superuser=True)

api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)
optional_api_key_header = APIKeyHeader(name='X-API-Key', auto_error=False)

APIKeyHeaderDep = Annotated[str, Depends(api_key_header)]
OptionalAPIKeyDep = Annotated[str | None, Depends(optional_api_key_header)]
OptionalCurrentUserDep = Annotated[models.UP, Depends(optional_get_current_user)]


async def verify_api_key(
    db_session: AsyncSessionDep,
    api_key: APIKeyHeaderDep,
) -> ApiKey:
    query = select(ApiKey).where(ApiKey.key == api_key)
    result = await db_session.execute(query)
    row = result.fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid API Key',
            headers={'WWW-Authenticate': 'APIKey'},
        )

    return row[0]


async def get_auth(
    db_session: AsyncSessionDep,
    user: OptionalCurrentUserDep,
    api_key: OptionalAPIKeyDep,
) -> models.UP | None | ApiKey:
    if user:
        msg = f'Authenticated user: {user.email}'

        logger.debug(msg)

        return user

    if api_key:
        api_key = await verify_api_key(db_session, api_key)
        msg = f'Authenticated API key: id={api_key.uid}, name={api_key.partner_name}'

        logger.debug(msg)

        return api_key

    msg = 'Invalid authentication credentials'

    logger.warning(msg)

    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail=msg,
    )
