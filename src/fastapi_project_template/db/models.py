from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, DateTime, ForeignKey, BIGINT, UniqueConstraint
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression
from sqlalchemy.sql.ddl import CreateColumn

from fastapi_project_template.db import Base


class UTCNow(expression.FunctionElement):
    type = DateTime()


@compiles(UTCNow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(CreateColumn, 'postgresql')
def use_identity(element, compiler, **kw):
    result = compiler.visit_create_column(element, **kw).replace('SERIAL', 'INT GENERATED BY DEFAULT AS IDENTITY')

    return result.replace('BIGSERIAL', 'BIGINT GENERATED BY DEFAULT AS IDENTITY')


class BaseDBModel:
    id = Column(BIGINT, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=UTCNow())
    updated_at = Column(DateTime(timezone=True), onupdate=UTCNow())


class Group(BaseDBModel, Base):
    __tablename__ = 'groups'

    name = Column(String, nullable=False)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    password_changed_at = Column(DateTime(timezone=True))


class UserGroup(BaseDBModel, Base):
    __tablename__ = 'user_groups'

    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    group_id = Column(BIGINT, ForeignKey('groups.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'group_id', name='uq_user_groups'),
    )
