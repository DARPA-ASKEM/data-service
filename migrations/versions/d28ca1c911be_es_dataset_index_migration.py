"""ES Dataset Index Migration

Revision ID: d28ca1c911be
Revises: b3bdf1b266ff
Create Date: 2023-09-26 14:29:46.125604

"""
import json

import sqlalchemy as sa

# pylint: disable=no-member, invalid-name
from alembic import op

# Elasticsearch operators such as es.create_index, es.remove_index, es.update_index_schema, es.bulk_load_index_from_jsonl, etc
from migrations import es

# revision identifiers, used by Alembic.
revision = "d28ca1c911be"
down_revision = "b3bdf1b266ff"
branch_labels = None
depends_on = None


def upgrade() -> None:
    es.update_index_schema(
        index_name=es.normalize_index("dataset"), new_schema=new_schema
    )


def downgrade() -> None:
    es.update_index_schema(
        index_name=es.normalize_index("dataset"), new_schema=orig_schema
    )


orig_schema = json.loads(
    """{
    "properties": {
      "timestamp": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss"
      }
    }
  }
"""
)

new_schema = json.loads(
    """{
    "properties": {
      "timestamp": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss"
      },
      "columns.metadata": {
        "type": "object",
        "enabled": false
      }
    }
  }
"""
)
