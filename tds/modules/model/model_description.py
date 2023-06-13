"""
TDS Model Description
"""
from datetime import datetime
from typing import Optional

from pydantic import Field

from tds.db.base import TdsModel


class ModelDescription(TdsModel):
    """
    Model description for list response.
    """

    name: str
    description: str
    model_schema: Optional[str] = Field(alias="schema")
    timestamp = datetime
    model_version: str

    class Config:
        """
        Model Description Config
        """

        schema_extra = {
            "example": {
                "name": "Model Name",
                "description": "Model Description",
                "model": {},
                "schema": "Model Schema",
                "model_version": "1.0",
            }
        }
