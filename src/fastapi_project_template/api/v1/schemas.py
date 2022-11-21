import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, UUID4


class UserRead(schemas.BaseUser[uuid.UUID]):
    group_id: Optional[int] = None


class UserCreate(schemas.BaseUserCreate):
    group_id: Optional[int] = None


class UserUpdate(schemas.BaseUserUpdate):
    group_id: Optional[int] = None


class UserGroupSearchParams(BaseModel):
    name: Optional[str]


class UserGroup(BaseModel):
    id: int
    name: str


class UserItem(BaseModel):
    id: UUID4
    email: str
    group_id: Optional[int]
    is_active: bool
    is_superuser: bool
    is_verified: bool
