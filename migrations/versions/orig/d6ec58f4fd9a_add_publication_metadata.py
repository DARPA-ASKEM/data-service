"""Add publication metadata.

Revision ID: d6ec58f4fd9a
Revises: 1a3cf96fb50f
Create Date: 2023-07-11 17:14:23.697577

"""
import sqlalchemy as sa

# pylint: disable=no-member, invalid-name
from alembic import op

# revision identifiers, used by Alembic.
revision = "d6ec58f4fd9a"
down_revision = "1a3cf96fb50f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("publication", sa.Column("publication_data", sa.JSON, nullable=True))


def downgrade() -> None:
    op.drop_column("publication", "publication_data")
