from fastapi import APIRouter
from fastapi_users import fastapi_users

from fastapi_project_template.api.v1.auth import auth_backend
from fastapi_project_template.api.v1.schemas import UserRead, UserUpdate

auth_router = fastapi_users.get_auth_router(auth_backend, requires_verification=True)
users_router = fastapi_users.get_users_router(
    user_schema=UserRead,
    user_update_schema=UserUpdate,
    requires_verification=True
)
router = APIRouter()
