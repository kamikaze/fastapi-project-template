import contextvars
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

correlation_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar('correlation_id')


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get('X-Correlation-ID', str(uuid4()))
        correlation_id_ctx.set(correlation_id)

        response = await call_next(request)
        response.headers['X-Correlation-ID'] = correlation_id
        return response
