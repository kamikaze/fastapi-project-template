from contextvars import ContextVar

from fastapi_project_template._cmod import c_fib
from fastapi_project_template._rustmod import rust_fib

try:
    from fastapi_project_template._version import __version__
except ImportError:
    __version__ = 'unknown'

ctx_correlation_id: ContextVar[str | None] = ContextVar('correlation_id', default=None)

__all__ = ['c_fib', 'ctx_correlation_id', 'rust_fib']
