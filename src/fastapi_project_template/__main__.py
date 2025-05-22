import logging.config

import uvicorn
from uvicorn.config import LOGGING_CONFIG

from fastapi_project_template import c_fib, rust_fib
from fastapi_project_template.api.http import app
from fastapi_project_template.conf import settings

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


logger.info(f'{c_fib(10)=}')
logger.info(f'{rust_fib(10)=}')
logger.info('Starting uvicorn.')
uvicorn.run(
    app,
    host=settings.service_addr,
    port=settings.service_port,
    forwarded_allow_ips='*',
    proxy_headers=True,
    log_config=LOGGING_CONFIG,
)
