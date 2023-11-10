import uvicorn
from fastapi_project_template.extmod import c_fib
from uvicorn.config import LOGGING_CONFIG

from fastapi_project_template.api.http import app
from fastapi_project_template.conf import settings


print(f'{c_fib(10)=}')
uvicorn.run(app, host=settings.service_addr, port=settings.service_port, proxy_headers=True, log_config=LOGGING_CONFIG)
