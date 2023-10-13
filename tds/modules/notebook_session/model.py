"""
TDS  Notebook Session Data Model Definition.
"""
from typing import Optional

from tds.db.base import BaseElasticSearchModel


class NotebookSession(BaseElasticSearchModel):
    """
    NotebookSession Data Model
    """

    name: Optional[str]
    description: Optional[str]
    data: dict

    _index = "notebook_session"

    class Config:
        """
        NotebookSession Data Model Swagger Example
        """

        schema_extra = {"example": {}}
