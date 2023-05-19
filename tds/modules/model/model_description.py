"""
TDS Model Description
"""
from pydantic import Field

from tds.db.base import TdsModel


class ModelDescription(TdsModel):
    """
    Model description for list response.
    """

    name: str
    description: str
    model_schema: str = Field(alias="schema")
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
