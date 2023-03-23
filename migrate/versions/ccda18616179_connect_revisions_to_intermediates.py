"""Connect revisions to intermediates

Revision ID: ccda18616179
Revises: 1f5853959c65
Create Date: 2023-03-22 15:26:05.133860

"""
# pylint: disable=no-member, invalid-name

from alembic import op
from sqlalchemy import text
from sqlalchemy.orm.session import Session

# revision identifiers, used by Alembic.
revision = "ccda18616179"
down_revision = "1f5853959c65"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Attach Models to intermediates instead of ModelRevisions
    """
    with Session(bind=op.get_bind()) as session:
        statement = text(
            """
        update provenance p set left_type='Model', 
        "left"=( select sub.right from provenance as sub
            where sub.left_type='Model'
            and sub.relation_type='BEGINS_AT'
            and sub.right_type='ModelRevision'
            and sub.right=p.left
            limit 1
        ) 
        where left_type='ModelRevision' 
        and relation_type='REINTERPRETS' and right_type='Intermediate';
        """
        )
        session.execute(statement)
        session.commit()


def downgrade() -> None:
    """
    [BROKEN] Data does not downgrade
    """
