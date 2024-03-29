from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    logging_level: str = 'INFO'
    logging_format: str = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    db_dsn: PostgresDsn | None = None
    service_addr: str = '0.0.0.0'
    service_port: int = 8080
    bootstrap_user_email: str | None = None
    bootstrap_user_password: SecretStr | None = None
    auth_secret: SecretStr = 'TODO-REPLACE'
    timezone: str = 'UTC'


settings = Settings()
