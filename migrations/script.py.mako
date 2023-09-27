"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
# pylint: disable=no-member, invalid-name
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}
# Elasticsearch operators such as es.create_index, es.remove_index, es.update_index_mapping, es.bulk_load_index_from_jsonl, etc
from migrations import es

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
