from pydantic import BaseSettings, PostgresDsn, SecretStr


class Settings(BaseSettings):
    logging_level: str = 'INFO'
    logging_format: str = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    db_dsn: PostgresDsn = None
    service_addr: str = '127.0.0.1'
    service_port: int = 8080
    alembic_auto_upgrade: bool = False
    alembic_config: str = 'alembic.ini'
    bootstrap_user_email: str | None = None
    auth_secret: SecretStr = 'TODO-REPLACE'


settings = Settings()
