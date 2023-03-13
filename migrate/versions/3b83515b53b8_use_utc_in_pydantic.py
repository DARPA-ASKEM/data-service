"""Use UTC in Pydantic

Revision ID: 3b83515b53b8
Revises: 1f5853959c65
Create Date: 2023-03-13 12:32:44.369730

"""
# pylint: disable=no-member, invalid-name

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3b83515b53b8"
down_revision = "1f5853959c65"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Remove timestamp defaults
    """
    op.alter_column("dataset", "timestamp", server_default=None)
    op.alter_column("intermediate", "timestamp", server_default=None)
    op.alter_column("model_description", "timestamp", server_default=None)
    op.alter_column("model_runtime", "timestamp", server_default=None)
    op.alter_column("model_state", "timestamp", server_default=None)
    op.alter_column("project", "timestamp", server_default=None)
    op.alter_column("provenance", "timestamp", server_default=None)
    op.alter_column("simulation_run", "timestamp", server_default=None)
    op.alter_column("software", "timestamp", server_default=None)


def downgrade() -> None:
    """
    Default timestamps to current time on the server
    """

    op.alter_column(
        "dataset",
        "timestamp",
        existing_type=postgresql.TIMESTAMP(),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )
    op.alter_column(
        "intermediate",
        "timestamp",
        existing_type=postgresql.TIMESTAMP(),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )
    op.alter_column(
        "model_description",
        "timestamp",
        existing_type=postgresql.TIMESTAMP(),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )
    op.alter_column(
        "model_runtime",
        "timestamp",
        existing_type=postgresql.TIMESTAMP(),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )
    op.alter_column(
        "model_state",
        "timestamp",
        existing_type=postgresql.TIMESTAMP(),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )
    op.alter_column(
        "project",
        "timestamp",
        existing_type=postgresql.TIMESTAMP(),
        server_default=sa.text("now()"),
        existing_nullable=True,
    )
    op.alter_column(
        "provenance",
        "timestamp",
        existing_type=postgresql.TIMESTAMP(),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )
    op.alter_column(
        "simulation_run",
        "timestamp",
        existing_type=postgresql.TIMESTAMP(),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )
    op.alter_column(
        "software",
        "timestamp",
        existing_type=postgresql.TIMESTAMP(),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )
