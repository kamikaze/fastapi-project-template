from functools import wraps
from inspect import signature

from fastapi import HTTPException, status


def _handle_exceptions_helper(status_code, *args):
    if args:
        raise HTTPException(status_code=status_code, detail=args[0])
    else:
        raise HTTPException(status_code=status_code)


def handle_exceptions(func):
    signature(func)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except PermissionError as e:
            return _handle_exceptions_helper(status.HTTP_401_UNAUTHORIZED, *e.args)
        except LookupError as e:
            return _handle_exceptions_helper(status.HTTP_404_NOT_FOUND, *e.args)
        except ValueError as e:
            return _handle_exceptions_helper(status.HTTP_400_BAD_REQUEST, *e.args)

    return wrapper
