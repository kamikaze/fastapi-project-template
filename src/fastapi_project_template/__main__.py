import uvicorn

from fastapi_project_template.api.http import app
from fastapi_project_template.conf import settings

uvicorn.run(app, host=settings.service_addr, port=settings.service_port)
