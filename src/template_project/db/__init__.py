from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base


metadata = MetaData()
Base = declarative_base(metadata=metadata)


async def is_healthy(pg) -> bool:
    return await pg.fetchval('SELECT 1 FROM alembic_version;') == 1
