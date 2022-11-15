"""
Provides the API interface for software
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from tds.autogen import schema


class Software(schema.Software):
    class Config:
        orm_mode = True
