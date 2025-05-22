from fastapi import APIRouter

from fastapi_project_template.api.v1.auth import auth_backend, fastapi_users
from fastapi_project_template.api.v1.schemas import UserRead, UserUpdate

auth_router = fastapi_users.get_auth_router(auth_backend, requires_verification=True)
users_router = fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True)
# auth_register_router = fastapi_users.get_register_router(UserRead, UserCreate)


health_router = APIRouter(tags=['health'])
report_router = APIRouter(tags=['reports'])
