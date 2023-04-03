import logging
import os

from alembic import command
from alembic.config import Config

logger = logging.getLogger(__name__)


def run_db_migrations(config, dsn: str, script_location: str) -> None:
    logger.info(f'Running DB migrations in {script_location}')
    original_wd = os.getcwd()
    os.chdir(script_location)
    alembic_cfg = Config(config)
    alembic_cfg.attributes['configure_logger'] = False
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')
    os.chdir(original_wd)
