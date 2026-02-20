from collections.abc import Sequence

from pydantic import BaseModel, HttpUrl


class AppConfig(BaseModel):
    oidc_authority_url: HttpUrl | None
    oidc_client_id: str | None
    oidc_redirect_uri: str | None = None
    oidc_scope: Sequence[str] | None = None
    oidc_audience: Sequence[str] | None = None
