"""
Provides the API interface for framework
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from tds.autogen import schema


class ModelFramework(schema.ModelFramework):
    class Config:
        orm_mode = True
