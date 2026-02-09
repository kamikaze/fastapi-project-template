import decimal
from collections.abc import Sequence
from typing import Annotated

from pydantic import BeforeValidator, HttpUrl, RedisDsn, SecretStr
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

    service_addr: str = '0.0.0.0'  # noqa: S104
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

    opa_url: HttpUrl | None = None


class RODBSettings(DBSettings):
    model_config = SettingsConfigDict(env_prefix='RO_DB_')


ro_db_settings = RODBSettings()
settings = Settings()


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {'format': settings.logging_format},
        'json': {
            '()': 'python3_commons.log.formatters.JSONFormatter',
        },
    },
    'filters': {
        'info_and_below': {'()': 'python3_commons.log.filters.filter_maker', 'level': 'INFO'},
        'correlation_id': {'()': 'fastapi_project_template.log.filters.CorrelationIDFilter'},
        'add_client_info': {'()': 'fastapi_project_template.log.filters.LogContextFilter'},
    },
    'handlers': {
        'default_stdout': {
            'level': settings.logging_level,
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': settings.logging_formatter,
            'filters': [
                'info_and_below',
                'correlation_id',
                'add_client_info',
            ],
        },
        'default_stderr': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': settings.logging_formatter,
            'filters': [
                'correlation_id',
                'add_client_info',
            ],
        },
    },
    'loggers': {
        '': {
            'handlers': [
                'default_stderr',
                'default_stdout',
            ],
        },
        'fastapi_project_template': {
            'handlers': [
                'default_stderr',
                'default_stdout',
            ],
            'level': settings.logging_level,
            'propagate': False,
        },
        '__main__': {
            'handlers': [
                'default_stderr',
                'default_stdout',
            ],
            'level': settings.logging_level,
            'propagate': False,
        },
    },
}
