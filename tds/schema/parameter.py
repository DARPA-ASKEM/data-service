"""
Allows manipulation of independent parameters
"""
# pylint: disable=missing-class-docstring

from typing import Optional

from pydantic import BaseModel


class IndependentParameter(BaseModel):
    curie: Optional[str] = None

    class Config:
        orm_mode = True
