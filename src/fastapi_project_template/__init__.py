import importlib.metadata
from contextvars import ContextVar

from fastapi_project_template._cmod import c_fib
from fastapi_project_template._rustmod import rust_fib

try:
    dist_name = __name__
    __version__ = importlib.metadata.version(dist_name)
except importlib.metadata.PackageNotFoundError:
    __version__ = 'unknown'

ctx_correlation_id: ContextVar[str | None] = ContextVar('correlation_id', default=None)

__all__ = ['ctx_correlation_id', 'c_fib', 'rust_fib']
