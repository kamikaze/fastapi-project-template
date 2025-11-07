from typing import Annotated

from fastapi import Header, Request


def get_client_ip(request: Request, x_forwarded_for: Annotated[str | None, Header()] = None) -> str:
    if x_forwarded_for:
        return x_forwarded_for

    return request.client.host
