import argparse
import asyncio
import logging.config

from fastapi_users.exceptions import UserAlreadyExists

from fastapi_project_template.api.users import get_user_manager_context
from fastapi_project_template.api.v1.schemas import UserCreate
from fastapi_project_template.conf import settings
from fastapi_project_template.db import database
from fastapi_project_template.db.user_db_helpers import get_async_session_context, get_user_db_context

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'fastapi_project_template.logging.formatter.JSONFormatter',
        },
    },
    'filters': {
        'info_and_below': {
            '()': 'fastapi_project_template.logging.filters.filter_maker',
            'level': 'INFO'
        }
    },
    'handlers': {
        'default_stdout': {
            'level': settings.logging_level,
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
            'filters': ['info_and_below', ],
        },
        'default_stderr': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default_stderr', 'default_stdout', ],
        },
        'fastapi_project_template': {
            'handlers': ['default_stderr', 'default_stdout', ],
            'level': settings.logging_level,
            'propagate': False,
        }
    }
})

logger = logging.getLogger(__name__)


async def create_superuser():
    await database.connect()

    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=settings.bootstrap_user_email,
                            password=settings.bootstrap_user_password.get_secret_value(),
                            is_superuser=True,
                            is_active=True,
                            is_verified=True
                        )
                    )
                    logger.info(f'User created: {settings.bootstrap_user_email}')
    except UserAlreadyExists:
        logger.warning(f'User already exists: {settings.bootstrap_user_email}')
    finally:
        await database.disconnect()


def get_parsed_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--job', type=str)

    args, args_other = parser.parse_known_args()

    return args


async def main():
    args = get_parsed_args()
    job_mapping = {
        'create_superuser': create_superuser,
    }

    try:
        job = job_mapping[args.job]
    except KeyError:
        logger.error(f'Unknown job: "{args.job}"')
    else:
        await job()

    logger.info(f'Job {args.job} finished')


if __name__ == '__main__':
    asyncio.run(main())
