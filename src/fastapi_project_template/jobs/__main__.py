import argparse
import asyncio
import logging.config
from argparse import Namespace

from fastapi_project_template.conf import settings

logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                '()': 'python3_commons.log.formatters.JSONFormatter',
            },
        },
        'filters': {'info_and_below': {'()': 'python3_commons.log.filters.filter_maker', 'level': 'INFO'}},
        'handlers': {
            'default_stdout': {
                'level': settings.logging_level,
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'default',
                'filters': [
                    'info_and_below',
                ],
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
                'handlers': [
                    'default_stderr',
                    'default_stdout',
                ],
            },
            'cash_backend': {
                'handlers': [
                    'default_stderr',
                    'default_stdout',
                ],
                'level': settings.logging_level,
                'propagate': False,
            },
            'aioworldline': {
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
)

logger = logging.getLogger(__name__)


def get_parsed_args() -> Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--job', type=str)

    args, _ = parser.parse_known_args()

    return args


async def poc() -> None:
    return None


async def main() -> None:
    args = get_parsed_args()
    job_mapping = {
        'poc': poc,
    }

    try:
        job = job_mapping[args.job]
    except KeyError:
        logger.exception('Unknown job: "%s"', {args.job})
    else:
        await job()

    logger.info('Job "%s" finished', args.job)


asyncio.run(main())
