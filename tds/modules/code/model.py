"""
TDS Code Data Model Definition.
"""
from typing import Optional

from tds.db.base import TdsModel
from tds.db.enums import ProgrammingLanguage


class Code(TdsModel):
    """
    Code Data Model
    """

    name: str
    description: str
    filename: str
    repo_url: Optional[str]
    language: ProgrammingLanguage
    metadata: Optional[dict]

    _index = "code"

    class Config:
        """
        Code Data Model Swagger Example
        """

        schema_extra = {
            "example": {
                "name": "Example Model Code",
                "description": "Example of a Python based code object for a model",
                "filename": "code.py",
                "language": "python",
            }
        }
