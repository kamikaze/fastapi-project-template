import importlib.metadata
from contextvars import ContextVar

from fastapi_project_template._ext import c_fib, rust_fib

try:
    __version__ = importlib.metadata.version('fastapi-project-template')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.0'

ctx_correlation_id: ContextVar[str | None] = ContextVar('correlation_id', default=None)

__all__ = (
    '__version__',
    'c_fib',
    'ctx_correlation_id',
    'rust_fib',
)
