"""
tds.schema.provenance - API facing provenance schema
"""

# pylint: disable=missing-class-docstring
from tds.autogen import schema


class Provenance(schema.Provenance):
    class Config:
        orm_mode = True
