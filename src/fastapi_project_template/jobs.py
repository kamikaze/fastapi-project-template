import argparse
import asyncio
import logging.config

from fastapi_project_template.conf import settings


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': settings.logging_format,
        },
    },
    'handlers': {
        'default': {
            'level': settings.logging_level,
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': settings.logging_level,
            'propagate': True,
        }
    }
})

logger = logging.getLogger(__name__)


def get_parsed_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--job', type=str)

    args, args_other = parser.parse_known_args()

    return args


async def foo():
    logger.info('Foo')


async def bar():
    logger.info('Bar')


async def main():
    args = get_parsed_args()
    job_mapping = {
        'foo': foo,
        'bar': bar,
    }

    try:
        await job_mapping[args.job]()
    except KeyError:
        logger.error(f'Unknown job: "{args.job}"')


if __name__ == '__main__':
    asyncio.run(main())
