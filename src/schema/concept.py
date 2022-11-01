"""
schema.dataset - Provides the API interface for concepts.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from pydantic import BaseModel
from src.autogen import schema


class Concept(BaseModel):
    term_id: str
    status: schema.Importance
