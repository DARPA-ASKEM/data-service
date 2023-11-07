"""Adds equations index

Revision ID: b9e1a8e285ba
Revises: d55d79761071
Create Date: 2023-11-02 20:29:07.225750

"""
import sqlalchemy as sa

# pylint: disable=no-member, invalid-name
from alembic import op

# Elasticsearch operators such as es.create_index, es.remove_index, es.update_index_mapping, es.bulk_load_index_from_jsonl, etc
from migrations import es

# revision identifiers, used by Alembic.
revision = "b9e1a8e285ba"
down_revision = "d55d79761071"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sqltext="""ALTER TYPE resourcetype ADD VALUE 'equations';""")
    op.execute(sqltext="""ALTER TYPE provenancetype ADD VALUE 'Equation';""")

    es.create_index(index_name=es.normalize_index("equation"), mapping={})


def downgrade() -> None:
    es.remove_index(index_name=es.normalize_index("equation"))
