import uuid
from collections.abc import Sequence

from fastapi_users import schemas
from pydantic import UUID4, BaseModel, ConfigDict


class UserRead(schemas.BaseUser[uuid.UUID]):
    model_config = ConfigDict(from_attributes=True)

    group_id: int | None = None


class UserCreate(schemas.BaseUserCreate):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str | None = None
    password: str
    group_id: int | None = None


class UserUpdate(schemas.BaseUserUpdate):
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
    oidc_authority_url: str | None
    oidc_client_id: str | None
    oidc_redirect_uri: str | None = None
    oidc_scopes: Sequence[str] | None = None
