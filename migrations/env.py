import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

import alembic_postgresql_enum as alembic_postgresql_enum  # noqa: PLC0414
from alembic import context
from python3_commons.conf import DBSettings
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine.base import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from fastapi_project_template.db.models import Base

sys.path.append(str(Path.cwd()))

config = context.config

if config.attributes.get('configure_logger', True) and config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    db_settings = DBSettings()

    return str(db_settings.dsn)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = get_url()
    connectable = AsyncEngine(
        engine_from_config(
            configuration,
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        tsk = loop.create_task(run_migrations_online())
        tsk.add_done_callback(lambda t: t.result())
    else:
        asyncio.run(run_migrations_online())
