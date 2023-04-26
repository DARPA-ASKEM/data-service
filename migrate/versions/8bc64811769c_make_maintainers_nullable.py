"""Make maintainers nullable

Revision ID: 8bc64811769c
Revises: ccda18616179
Create Date: 2023-04-26 14:11:36.427853

"""
# pylint: disable=no-member, invalid-name
import sqlalchemy as sa
from alembic import op

revision = "8bc64811769c"
down_revision = "ccda18616179"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Remove need for maintainer
    """
    op.alter_column("dataset", "maintainer", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column(
        "dataset",
        "deprecated",
        existing_type=sa.BOOLEAN(),
        server_default="False",
        existing_nullable=True,
    )


def downgrade() -> None:
    """
    Make maintainers mandatory
    """
    op.alter_column("dataset", "maintainer", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column(
        "dataset",
        "deprecated",
        existing_type=sa.BOOLEAN(),
        server_default=None,
        existing_nullable=True,
    )
