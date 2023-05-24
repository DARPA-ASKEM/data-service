"""empty message

Revision ID: 139b9ec56f3e
Revises: b9e9469640b6
Create Date: 2023-05-24 10:09:39.628832

"""
# pylint: disable=no-member, invalid-name
from alembic import op
from sqlalchemy import text
from sqlalchemy.orm.session import Session

# revision identifiers, used by Alembic.
revision = "139b9ec56f3e"
down_revision = "b9e9469640b6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Attach Models to intermediates instead of ModelRevisions
    """
    with Session(bind=op.get_bind()) as session:
        statement = text(
            """update dataset set data_path = (annotations -> 'data_paths' -> 0);"""
        )
        session.execute(statement)
        session.commit()


def downgrade() -> None:
    """
    Not needed
    """
    pass
