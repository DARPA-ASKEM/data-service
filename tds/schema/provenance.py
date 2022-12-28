"""
tds.schema.provenance - API facing provenance schema
"""

from typing import Dict, Optional, Type

# pylint: disable=missing-class-docstring
from tds.autogen import schema


class Provenance(schema.Provenance):
    class Config:
        orm_mode = True


class ProvenancePayload:
    root_id: int
    root_type: schema.ProvenanceType
    search_type: schema.ProvenanceSearchTypes
