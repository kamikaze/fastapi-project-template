from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_dsn: Optional[str] = None
    alembic_auto_upgrade: bool = False
    alembic_config: str = 'alembic.ini'


settings = Settings()
