"""Connect revisions to intermediates

Revision ID: ccda18616179
Revises: 1f5853959c65
Create Date: 2023-03-22 15:26:05.133860

"""
# pylint: disable=no-member, invalid-name

from alembic import op
from sqlalchemy.orm.session import Session

from tds.autogen.orm import Provenance

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
        # This solution is not optimized for SQL; could be done in bulk
        rev_to_model = {
            entry.right: entry.left
            for entry in session.query(Provenance)
            .filter(
                Provenance.left_type == "Model",
                Provenance.relation_type == "BEGINS_AT",
                Provenance.right_type == "ModelRevision",
            )
            .all()
        }

        entries = (
            session.query(Provenance)
            .filter(
                Provenance.left_type == "ModelRevision",
                Provenance.relation_type == "REINTERPRETS",
                Provenance.right_type == "Intermediate",
            )
            .all()
        )

        for entry in entries:
            entry.update(
                {
                    Provenance.left_type: "Model",
                    Provenance.left: rev_to_model[entry.left],
                }
            )
        session.commit()


def downgrade() -> None:
    """
    [BROKEN] Data does not downgrade
    """
