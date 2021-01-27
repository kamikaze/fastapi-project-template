from typing import List

import sqlalchemy as sa
from asyncpg import UniqueViolationError

from template_project.db.models import DBRecord


async def get_db_records(database, order_by=None) -> List[dict]:
    return await database.fetch_all(sa.select([DBRecord]).order_by('id'))


async def get_db_record(database, pk: int) -> List[dict]:
    return await database.execute(sa.select([DBRecord]).get(pk))


async def create_db_record(database, fields: dict) -> int:
    query = sa.insert(DBRecord).values(**fields)

    try:
        return await database.execute(query)
    except UniqueViolationError as e:
        raise ValueError(str(e))
