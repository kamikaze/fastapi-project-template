import logging

from fastapi_project_template.middleware.correlation_id import correlation_id_ctx
from fastapi_project_template.middleware.log_context import log_context


class LogContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if context := log_context.get() is None:
            log_context.set({})
        else:
            for key, value in context.items():
                if value:
                    setattr(record, key, value)

        return True


class CorrelationIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            correlation_id = correlation_id_ctx.get()
            if correlation_id:
                record.correlation_id = correlation_id
        except LookupError:
            pass

        return True
