import databases
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from fastapi_project_template.conf import settings

metadata = MetaData()
Base = declarative_base(metadata=metadata)
database = databases.Database(settings.db_dsn)


async def is_healthy(pg) -> bool:
    return await pg.fetchval('SELECT 1 FROM alembic_version;') == 1
