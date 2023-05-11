"""Add data_path to datasets

Revision ID: b9e9469640b6
Revises: 8bc64811769c
Create Date: 2023-05-11 16:33:41.553913

"""
# pylint: disable=no-member, invalid-name
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b9e9469640b6"
down_revision = "8bc64811769c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add the data_path column
    """
    op.add_column("dataset", sa.Column("data_path", sa.String(), nullable=True))


def downgrade() -> None:
    """
    Drop the additional data_path column
    """
    op.drop_column("dataset", "data_path")
