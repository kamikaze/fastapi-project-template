import contextvars

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi_project_template.api.helpers import get_client_ip

log_context: contextvars.ContextVar[dict] = contextvars.ContextVar('log_context', default={})


class LogContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        context = {
            'client_ip': get_client_ip(request),
        }

        log_context.set(context)

        return await call_next(request)
