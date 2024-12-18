import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, CookieTransport, AuthenticationBackend

from fastapi_project_template.conf import settings
from fastapi_project_template.core.users import get_user_manager
from fastapi_project_template.db.models import User

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.auth_secret.get_secret_value(), lifetime_seconds=3600)


auth_backend = AuthenticationBackend(name='userauth', transport=cookie_transport, get_strategy=get_jwt_strategy)
auth_backends = [auth_backend, ]
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    auth_backends
)
get_current_user = fastapi_users.current_user(active=True)
get_current_superuser = fastapi_users.current_user(active=True, superuser=True)
