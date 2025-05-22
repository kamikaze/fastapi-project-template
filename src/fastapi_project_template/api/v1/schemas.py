import uuid

from fastapi_users import schemas
from pydantic import UUID4, BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    group_id: int | None = None

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str | None = None
    password: str
    group_id: int | None = None

    class Config:
        from_attributes = True


class UserUpdate(schemas.BaseUserUpdate):
    group_id: int | None = None

    class Config:
        from_attributes = True


class UserGroupSearchParams(BaseModel):
    name: str | None

    class Config:
        from_attributes = True


class UserGroupItem(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserItem(BaseModel):
    id: UUID4
    email: str
    group_id: int | None
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        from_attributes = True
