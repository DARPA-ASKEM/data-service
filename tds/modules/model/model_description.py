"""
TDS Model Description
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from tds.db.base import TdsModel


class Header(BaseModel):
    """
    Header object for AMR
    """

    name: str
    description: str
    model_schema: Optional[str] = Field(alias="schema")
    schema_name: Optional[str]
    model_version: str


class ModelDescription(TdsModel):
    """
    Model description for list response.
    """

    header: Header
    username: Optional[str]
    timestamp: datetime = (
        datetime.now()
    )  # Assuming you meant it to be a default current datetime value

    class Config:
        """
        Model Description Config
        """

        schema_extra = {
            "example": {
                "header": {
                    "name": "Model Name",
                    "description": "Model Description",
                    "schema": "Model Schema",
                    "model_version": "1.0",
                },
                "username": "user123",
                "timestamp": "2023-08-30T00:00:00",  # Example datetime value in ISO format
            }
        }
