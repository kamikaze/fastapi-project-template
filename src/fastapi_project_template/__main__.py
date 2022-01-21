import uvicorn

from fastapi_project_template.api.http import app
from fastapi_project_template.conf import settings
from fastapi_project_template.extmod import c_fib

print(f'{c_fib(10)=}')
uvicorn.run(app, host=settings.service_addr, port=settings.service_port)
