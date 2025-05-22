import gettext
import logging
from pathlib import Path
from typing import Mapping, Sequence

import sqlalchemy as sa
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project_template.api.v1.schemas import UserItem
from fastapi_project_template.db.models import User, UserGroup

logger = logging.getLogger(__name__)
t = gettext.translation('base', Path(Path(__file__).parent, 'locale'), fallback=True, languages=['lv_LV'])
_ = t.gettext


async def get_users(
    session: AsyncSession, search: Mapping[str, str] | None = None, order_by: str | None = None
) -> Page[UserItem]:
    query = sa.select([User])
    result = await apaginate(session, query)

    return result


async def get_user(session: AsyncSession, user_id: str) -> UserItem:
    query = sa.select([User]).where(User.id == user_id)
    cursor = await session.execute(query)
    result = cursor.scalar()

    return result


async def get_user_groups(
    session: AsyncSession, search: Mapping[str, str] | None = None, order_by: str | None = None
) -> Sequence[UserGroup]:
    query = sa.select([UserGroup]).order_by(UserGroup.name)
    cursor = await session.execute(query)
    result = cursor.scalars()

    return result
