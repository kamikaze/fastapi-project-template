from granian import Granian
from granian.constants import Interfaces

from fastapi_project_template.conf import LOGGING_CONFIG, settings

server = Granian(
    'fastapi_project_template.api.http:app',
    address=settings.service_addr,
    port=settings.service_port,
    interface=Interfaces.ASGI,
    backlog=4096,
    workers=1,
    runtime_threads=2,
    runtime_blocking_threads=8,
    respawn_failed_workers=False,
    websockets=False,
    log_dictconfig=LOGGING_CONFIG,
    log_access=False,
    reload=False,
)

server.serve()
