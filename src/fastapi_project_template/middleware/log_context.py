import contextvars

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from fastapi_project_template.api.helpers import get_client_ip

log_context: contextvars.ContextVar[dict | None] = contextvars.ContextVar('log_context', default=None)


class LogContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        context = {
            'client_ip': get_client_ip(request),
        }

        log_context.set(context)

        return await call_next(request)
