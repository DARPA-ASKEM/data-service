"""
tds.schema.model - Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from typing import Optional

from tds.autogen import schema
from tds.schema.concept import Concept


class Model(schema.Model):
    concept: Optional[Concept]

    class Config:
        orm_mode = True
