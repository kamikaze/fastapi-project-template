import asyncio
import logging
import os
import pathlib
from functools import wraps
from inspect import signature
from typing import List, Optional

from alembic import command
from alembic.config import Config
from asyncpg import CannotConnectNowError
from databases import Database
from fastapi import FastAPI, Query, status, HTTPException

from template_project import core
from template_project.api.models import DBRecord
from template_project.conf import settings

logger = logging.getLogger(__name__)
app = FastAPI()
database = Database(settings.db_dsn)


def _handle_exceptions_helper(status_code, *args):
    if args:
        raise HTTPException(status_code=status_code, detail=args[0])
    else:
        raise HTTPException(status_code=status_code)


def handle_exceptions(func):
    signature(func)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except PermissionError as e:
            return _handle_exceptions_helper(status.HTTP_401_UNAUTHORIZED, *e.args)
        except LookupError as e:
            return _handle_exceptions_helper(status.HTTP_404_NOT_FOUND, *e.args)
        except ValueError as e:
            return _handle_exceptions_helper(status.HTTP_400_BAD_REQUEST, *e.args)

    return wrapper


def run_db_migrations(config, dsn: str, script_location: str) -> None:
    logger.info(f'Running DB migrations in {script_location}')
    original_wd = os.getcwd()
    os.chdir(script_location)
    alembic_cfg = Config(config)
    alembic_cfg.attributes['configure_logger'] = False
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')
    os.chdir(original_wd)


@app.on_event('startup')
async def startup():
    logger.info('Waiting for services')
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
            run_db_migrations(settings.alembic_config, settings.db_dsn, f'{script_location}/../db')
        else:
            logger.info('Automatic DB migration is disabled')
    except Exception as e:
        logger.error(f'Automatic DB migration failed: {e}')


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/db_records', response_model=List[DBRecord])
@handle_exceptions
async def get_db_records(order_by: Optional[List[str]] = Query(None, alias='orderBy')):
    return await core.get_db_records(database, order_by)


@app.get('/db_records/{pk}')
@handle_exceptions
async def get_db_record(pk: int) -> DBRecord:
    return await core.get_db_record(database, pk)
