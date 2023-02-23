"""Attach models to intermediates

Revision ID: eee465a0b5a2
Revises: 1f5853959c65
Create Date: 2023-02-23 11:40:22.947651

"""

# pylint: disable=no-member, invalid-name
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "eee465a0b5a2"
down_revision = "1f5853959c65"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Attach models to intermediates instead model revisions
    attaching to intermediates
    """


def downgrade() -> None:
    """
    Map revisions back to intermidates
    """
