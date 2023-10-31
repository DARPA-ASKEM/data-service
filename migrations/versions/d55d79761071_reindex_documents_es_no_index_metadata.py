"""Reindex documents es no-index metadata

Revision ID: d55d79761071
Revises: b796846784ce
Create Date: 2023-10-31 14:04:39.990958

"""
import json

import sqlalchemy as sa

# pylint: disable=no-member, invalid-name
from alembic import op

# Elasticsearch operators such as es.create_index, es.remove_index, es.update_index_mapping, es.bulk_load_index_from_jsonl, etc
from migrations import es

# revision identifiers, used by Alembic.
revision = "d55d79761071"
down_revision = "b796846784ce"
branch_labels = None
depends_on = None


def upgrade() -> None:
    es.update_index_mapping(
        index_name=es.normalize_index("dataset"), new_mapping=new_mapping
    )


def downgrade() -> None:
    es.update_index_mapping(
        index_name=es.normalize_index("dataset"), new_mapping=orig_mapping
    )


orig_mapping = json.loads(
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

new_mapping = json.loads(
    """{
    "properties": {
      "timestamp": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss"
      },
      "columns.metadata": {
        "type": "object",
        "enabled": false
      },
      "metadata": {
        "type": "object",
        "enabled": false
      }
    }
  }
"""
)
