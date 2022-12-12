import asyncio
import datetime
import logging
import os
import pathlib

from alembic import command
from alembic.config import Config
from asyncpg import CannotConnectNowError

from fastapi_project_template.conf import settings

logger = logging.getLogger(__name__)


def date_from_string(string: str, fmt: str = '%d.%m.%Y') -> datetime.date:
    try:
        return datetime.datetime.strptime(string, fmt).date()
    except ValueError:
        return datetime.date.fromisoformat(string)


def datetime_from_string(string: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(string, '%d.%m.%Y %H:%M:%S')
    except ValueError:
        return datetime.datetime.fromisoformat(string)


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + datetime.timedelta(days=n)


def run_db_migrations(config, dsn: str, script_location: str) -> None:
    logger.info(f'Running DB migrations in {script_location}')
    original_wd = os.getcwd()
    os.chdir(script_location)
    alembic_cfg = Config(config)
    alembic_cfg.attributes['configure_logger'] = False
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')
    os.chdir(original_wd)


async def connect_to_db(database):
    logger.info('Waiting for services')
    logger.debug(f'DB_DSN: {settings.db_dsn}')
    timeout = 0.001
    total_timeout = 0

    for i in range(15):
        try:
            await database.connect()
        except (ConnectionRefusedError, CannotConnectNowError):
            timeout *= 2
            await asyncio.sleep(timeout)
            total_timeout += timeout
        else:
            break
    else:
        msg = f'Unable to connect database for {int(total_timeout)}s'
        logger.error(msg)
        raise ConnectionRefusedError(msg)

    try:
        if settings.alembic_auto_upgrade and settings.alembic_config:
            script_location = str(pathlib.Path(__file__).parent.absolute())
            run_db_migrations(settings.alembic_config, settings.db_dsn, f'{script_location}/db')
        else:
            logger.info('Automatic DB migration is disabled')
    except Exception as e:
        logger.error(f'Automatic DB migration failed: {e}')


def tries(times):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            for time in range(times if times > 0 else 1):
                # noinspection PyBroadException
                try:
                    return await f(*args, **kwargs)
                except Exception as exc:
                    if time >= times:
                        raise exc

        return wrapper

    return func_wrapper
