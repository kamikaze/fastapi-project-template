import gettext
import logging
from pathlib import Path
from typing import Mapping, Optional, Sequence

import sqlalchemy as sa
from databases.backends.postgres import Record
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate

from fastapi_project_template.db.models import UserGroup, User

logger = logging.getLogger(__name__)
t = gettext.translation('base', Path(Path(__file__).parent, 'locale'), fallback=True, languages=['lv_LV'])
_ = t.gettext


async def get_users(database, search: Optional[Mapping[str, str]] = None,
                    order_by: Optional[str] = None) -> AbstractPage[Record]:
    query = sa.select([User])
    result = await paginate(database, query)

    return result


async def get_user(database, user_id: str) -> Record:
    query = sa.select([User]).where(User.id == user_id)

    return await database.fetch_row(query)


async def get_user_groups(database, search: Optional[Mapping[str, str]] = None,
                          order_by: Optional[str] = None) -> Sequence[Record]:
    query = sa.select([UserGroup]).order_by(UserGroup.name)
    result = await database.fetch_all(query)

    return result
