from collections.abc import Sequence
from uuid import UUID

from pydantic import UUID4, BaseModel, ConfigDict, HttpUrl


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: UUID
    group_id: int | None = None


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    group_id: int | None = None


class UserGroupSearchParams(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None


class UserGroupApiSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class UserApiSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    email: str
    group_id: int | None
    is_active: bool
    is_superuser: bool
    is_verified: bool


class AppConfig(BaseModel):
    oidc_authority_url: HttpUrl | None
    oidc_client_id: str | None
    oidc_redirect_uri: str | None = None
    oidc_scope: Sequence[str] | None = None
    oidc_audience: Sequence[str] | None = None
