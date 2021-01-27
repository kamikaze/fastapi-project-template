from typing import Optional

from fastapi_users import models
from pydantic import BaseModel, UUID4

from fastapi_project_template.db.models import User


class UserCreate(models.BaseUserCreate):
    group_id: Optional[int] = None


class UserUpdate(User, models.BaseUserUpdate):
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
