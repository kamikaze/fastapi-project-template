from datetime import datetime

from python3_commons.db import Base as Base
from python3_commons.db.models.auth import ApiKey as ApiKey
from python3_commons.db.models.common import BaseDBUUIDModel
from python3_commons.db.models.rbac import RBACApiKeyRole as RBACApiKeyRole
from python3_commons.db.models.rbac import RBACPermission as RBACPermission
from python3_commons.db.models.rbac import RBACRole as RBACRole
from python3_commons.db.models.rbac import RBACRolePermission as RBACRolePermission
from python3_commons.db.models.rbac import RBACUserRole as RBACUserRole
from python3_commons.db.models.users import User as User
from python3_commons.db.models.users import UserGroup as UserGroup
from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column


class UserProfile(BaseDBUUIDModel, Base):
    __tablename__ = 'user_profiles'

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    subject: Mapped[str] = mapped_column(String)
    issuer: Mapped[str] = mapped_column(String)
    name: Mapped[str | None] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String)

    __table_args__ = (
        Index('uix_user_profile_origin', subject, issuer, unique=True),
        Index('uix_user_profile_name', name, unique=True),
    )
