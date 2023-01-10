import uuid

from fastapi_users import schemas
from pydantic import BaseModel, UUID4


class UserRead(schemas.BaseUser[uuid.UUID]):
    group_id: int | None = None


class UserCreate(schemas.BaseUserCreate):
    group_id: int | None = None


class UserUpdate(schemas.BaseUserUpdate):
    group_id: int | None = None


class UserGroupSearchParams(BaseModel):
    name: str | None


class UserGroup(BaseModel):
    id: int
    name: str


class UserItem(BaseModel):
    id: UUID4
    email: str
    group_id: int | None
    is_active: bool
    is_superuser: bool
    is_verified: bool
