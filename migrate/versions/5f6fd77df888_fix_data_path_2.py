"""empty message

Revision ID: 5f6fd77df888
Revises: 139b9ec56f3e
Create Date: 2023-05-25 10:09:39.628832

"""
# pylint: disable=no-member, invalid-name
from alembic import op
from sqlalchemy import text
from sqlalchemy.orm.session import Session

# revision identifiers, used by Alembic.
revision = "5f6fd77df888"
down_revision = "139b9ec56f3e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Attach Models to intermediates instead of ModelRevisions
    """
    with Session(bind=op.get_bind()) as session:
        statement = text(
            """update dataset set data_path = trim(both '"' from data_path);"""
        )
        session.execute(statement)
        session.commit()


def downgrade() -> None:
    """
    Not needed
    """
