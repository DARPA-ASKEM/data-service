"""Add code project asset

Revision ID: f905fe63226c
Revises: d6ec58f4fd9a
Create Date: 2023-08-17 14:22:44.365574

"""
import sqlalchemy as sa

# pylint: disable=no-member, invalid-name
from alembic import op

# revision identifiers, used by Alembic.
revision = "f905fe63226c"
down_revision = "d6ec58f4fd9a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE public.resourcetype ADD VALUE 'code'")
        op.execute("ALTER TYPE public.taggabletype ADD VALUE 'code'")
        op.execute("ALTER TYPE public.provenancetype ADD VALUE 'Code'")


def downgrade() -> None:
    pass
