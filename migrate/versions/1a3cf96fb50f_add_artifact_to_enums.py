"""Add artifact to enums.

Revision ID: 1a3cf96fb50f
Revises: 895deab7e80c
Create Date: 2023-06-14 19:38:18.828648

"""
import sqlalchemy as sa

# pylint: disable=no-member, invalid-name
from alembic import op

# revision identifiers, used by Alembic.
revision = "1a3cf96fb50f"
down_revision = "895deab7e80c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE public.resourcetype ADD VALUE 'artifacts'")
        op.execute("ALTER TYPE public.taggabletype ADD VALUE 'artifacts'")
        op.execute("ALTER TYPE public.provenancetype ADD VALUE 'Artifact'")


def downgrade() -> None:
    pass
