"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
import sqlalchemy as sa
from alembic import op
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    schema_upgrades()
    data_upgrades()


def downgrade() -> None:
    data_downgrades()
    schema_downgrades()


def schema_upgrades() -> None:
    """schema upgrade migrations go here."""
    ${upgrades if upgrades else "pass"}


def schema_downgrades() -> None:
    """schema downgrade migrations go here."""
    ${downgrades if downgrades else "pass"}


def data_upgrades() -> None:
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades() -> None:
    """Add any optional data downgrade migrations here!"""
    pass
