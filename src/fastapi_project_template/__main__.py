import logging.config

import uvicorn

from fastapi_project_template.api.http import app
from fastapi_project_template.conf import settings
from fastapi_project_template.extmod import c_fib


LOGGING_CONFIG = {
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
}
logging.config.dictConfig(LOGGING_CONFIG)

print(f'{c_fib(10)=}')
uvicorn.run(app, host=settings.service_addr, port=settings.service_port, proxy_headers=True, log_config=LOGGING_CONFIG)
