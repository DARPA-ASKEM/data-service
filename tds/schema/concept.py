"""
Provides the API interface for concepts.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from pydantic import BaseModel

from tds.modules.concept.model import OntologicalField


class Concept(BaseModel):
    curie: str
    status: OntologicalField

    class Config:
        orm_mode = True
