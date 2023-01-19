"""
Allows manipulation of independent parameters
"""
# pylint: disable=missing-class-docstring

from typing import Optional

from tds.autogen import schema


class IndependentParameter(schema.ModelParameter):
    curie: Optional[str] = None

    class Config:
        orm_mode = True
