from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_dsn: Optional[str] = None
    service_addr: str = '127.0.0.1'
    service_port: int = 8080
    alembic_auto_upgrade: bool = False
    alembic_config: str = 'alembic.ini'
    bootstrap_user_email: Optional[str] = None
    auth_secret: str = 'TODO-REPLACE'


settings = Settings()
