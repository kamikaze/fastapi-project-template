from uuid import UUID

import sqlalchemy as sa
from python3_commons.auth import TokenData
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.db.models.users import UserProfile
from fastapi_project_template.services.users import dao
from fastapi_project_template.services.users.dto import UserUpdate


async def get_or_create_user_profile_by_token(db_session: AsyncSession, token: TokenData) -> UserProfile:
    try:
        user_profile = await dao.get_user_profile_by_token(db_session, token)
    except LookupError:
        user_profile = await dao.create_user_profile_from_token(db_session, token)

    return user_profile


async def update_user(db_session: AsyncSession, uid: UUID, user: UserUpdate) -> UserProfile:
    return await dao.update_user(db_session, uid, user)


def get_users_stmt(*, existing_only: bool = True) -> Select[tuple[UserProfile]]:
    stmt = sa.select(UserProfile).order_by(UserProfile.name)

    if existing_only:
        stmt = stmt.where(UserProfile.deleted_at.is_(None))

    return stmt
