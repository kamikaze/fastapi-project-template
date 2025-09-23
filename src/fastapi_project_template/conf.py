import decimal
from collections.abc import Sequence
from typing import Annotated

from pydantic import BeforeValidator, RedisDsn, SecretStr
from pydantic_settings import SettingsConfigDict
from python3_commons.conf import CommonSettings, DBSettings

global_decimal_context = decimal.getcontext()
global_decimal_context.rounding = decimal.ROUND_HALF_UP
decimal.DefaultContext = global_decimal_context


def parse_string_list(v: str | Sequence[str]) -> Sequence[str]:
    if isinstance(v, str):
        return tuple(map(str.strip, v.split(',')))

    return v


class Settings(CommonSettings):
    timezone: str = 'UTC'

    service_addr: str = '0.0.0.0'
    service_port: int = 8080
    allowed_origins: Annotated[Sequence[str] | tuple[str, ...], BeforeValidator(parse_string_list)] = ('*',)

    alembic_config: str = 'alembic.ini'

    bootstrap_user_email: str | None = None
    bootstrap_user_name: str | None = None
    bootstrap_user_password: SecretStr | None = None

    auth_secret: SecretStr = SecretStr('secret-string')

    valkey_dsn: RedisDsn | None = None
    valkey_sentinel_dsn: RedisDsn | None = None

    telegram_api_token: SecretStr | None = None
    telegram_chat_id: int | None = None


class RODBSettings(DBSettings):
    model_config = SettingsConfigDict(env_prefix='RO_DB_')


ro_db_settings = RODBSettings()
settings = Settings()
