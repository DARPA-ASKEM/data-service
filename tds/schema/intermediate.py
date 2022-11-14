"""
tds.schema.Intermediate - Provides the API interface for intermediates
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from tds.autogen import schema


class Intermediate(schema.Intermediate):
    class Config:
        orm_mode = True
