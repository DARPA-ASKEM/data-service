# pylint: skip-file
"""
Schema file from DBML autogen.
Skipping linter to prevent class docstring errors.
@TODO: Clean up file to pass linting.
"""
from typing import Optional

from pydantic import BaseModel

from tds.db.enums import ValueType


class Feature(BaseModel):
    id: Optional[int] = None
    dataset_id: Optional[int] = None
    description: Optional[str]
    display_name: Optional[str]
    name: str
    value_type: ValueType
