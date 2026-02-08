from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING

import msgspec
import sqlalchemy as sa
from python3_commons.db.models.users import User, UserGroup

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.sql.selectable import Select

logger = logging.getLogger(__name__)


class UserGroupItem(msgspec.Struct):
    id: int
    name: str


def get_users_stmt() -> Select:
    return sa.select(User)


async def get_user(session: AsyncSession, user_id: uuid.UUID) -> User:
    stmt = sa.select(User).where(User.uid == user_id)
    cursor = await session.execute(stmt)

    return cursor.scalar_one()


async def get_user_groups_stmt() -> Select[tuple[UserGroup]]:
    return sa.select(UserGroup).order_by(UserGroup.name)
