import importlib.metadata
from contextvars import ContextVar

try:
    dist_name = __name__
    __version__ = importlib.metadata.version(dist_name)
except importlib.metadata.PackageNotFoundError:
    __version__ = 'unknown'

ctx_correlation_id: ContextVar[str | None] = ContextVar('correlation_id', default=None)
