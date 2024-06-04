from typing import Sequence, Annotated

from pydantic import PostgresDsn, SecretStr, BeforeValidator
from pydantic_settings import BaseSettings


def parse_string_list(v: str) -> Sequence[str]:
    if v:
        return tuple(map(str.strip, v.split(',')))

    return tuple()


class Settings(BaseSettings):
    logging_level: str = 'INFO'
    logging_format: str = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    db_dsn: PostgresDsn | None = None
    service_addr: str = '0.0.0.0'
    service_port: int = 8080
    allowed_origins: Annotated[
        Sequence[str], BeforeValidator(parse_string_list)
    ] = ('*', 'http://localhost', 'http://localhost:3000',)
    bootstrap_user_email: str | None = None
    bootstrap_user_password: SecretStr | None = None
    auth_secret: SecretStr = 'TODO-REPLACE'
    timezone: str = 'UTC'


settings = Settings()
