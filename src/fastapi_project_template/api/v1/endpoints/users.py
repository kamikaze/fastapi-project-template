import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_commons.auth import get_token_verifier
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from python3_commons.auth import TokenData
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.api.v1.opa import opa_authorize
from fastapi_project_template.db import get_main_db_session
from fastapi_project_template.dto.users import UserCreate, UserProfile
from fastapi_project_template.services.users import users_service

logger = logging.getLogger(__name__)
JWKS = {}
get_verified_token = get_token_verifier(TokenData, JWKS)
AsyncSessionDep = Annotated[AsyncSession, Depends(get_main_db_session)]
TokenDep = Annotated[TokenData, Depends(get_verified_token)]


router = APIRouter(prefix='/users', tags=['Users'], dependencies=[Depends(opa_authorize)])


@router.get('/me')
async def get_current_user_profile(db_session: AsyncSessionDep, token: TokenDep) -> UserProfile:
    return await users_service.get_or_create_user_profile_by_token(db_session, token)


@router.get('')
async def get_user_list(db_session: AsyncSessionDep) -> Page[UserProfile]:
    stmt = users_service.get_users_stmt()

    return await apaginate(db_session, stmt)


@router.post('')
async def create_user(db_session: AsyncSessionDep, user: UserCreate) -> UserProfile:
    return await users_service.create_user(db_session, user.name, user.email)
