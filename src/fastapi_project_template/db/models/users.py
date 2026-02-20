from datetime import datetime

from python3_commons.db import Base
from python3_commons.db.models.common import BaseDBUUIDModel
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
