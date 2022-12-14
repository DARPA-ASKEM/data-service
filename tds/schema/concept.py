"""
Provides the API interface for concepts.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from pydantic import BaseModel

from tds.autogen import schema


class Concept(BaseModel):
    curie: str
    status: schema.OntologicalField

    class Config:
        orm_mode = True
