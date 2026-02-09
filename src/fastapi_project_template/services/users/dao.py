from uuid import uuid7

import sqlalchemy as sa
from python3_commons.auth import TokenData
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.db.models import UserProfile


async def get_user_profile_by_token(db_session: AsyncSession, token: TokenData) -> UserProfile:
    stmt = sa.select(UserProfile).where(UserProfile.subject == token.sub, UserProfile.issuer == token.iss)

    async with db_session.begin():
        cursor = await db_session.execute(stmt)

        if (user_profile := cursor.scalar_one_or_none()) is None:
            msg = 'User does not exist'
            raise LookupError(msg)

        return user_profile


async def create_user_profile_from_token(db_session: AsyncSession, token: TokenData) -> UserProfile:
    values = {'uid': uuid7(), 'subject': token.sub, 'issuer': token.iss}

    if email := token.email:
        values['email'] = email

    if username := token.preferred_username:
        values['name'] = username

    stmt = sa.insert(UserProfile).values(**values).returning(UserProfile)

    async with db_session.begin():
        cursor = await db_session.execute(stmt)

        return cursor.scalar_one()


async def create_user(db_session: AsyncSession, name: str, email: str) -> UserProfile:
    # subject and issuer are required by the model.
    # For manually created users, we might need some default or special values if they are not coming from OIDC
    # However, the requirement doesn't specify OIDC for THESE new users.
    # Assuming they will be OIDC users later, or we use 'manual' as issuer.
    values = {'uid': uuid7(), 'name': name, 'email': email, 'subject': f'manual:{email}', 'issuer': 'manual'}
    stmt = sa.insert(UserProfile).values(**values).returning(UserProfile)
    async with db_session.begin():
        cursor = await db_session.execute(stmt)
        return cursor.scalar_one()
