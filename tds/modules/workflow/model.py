"""
TDS Workflow Model Definition.
"""

from typing import List, Optional

from tds.db.base import TdsModel
from tds.settings import settings


class Workflow(TdsModel):
    """
    Workflow Data Model
    """

    name: str
    description: str

    _index = "workflow"
    concepts: Optional[List] = []
    exists = False

    def save(self):
        """
        Method saves the object to ElasticSearch.
        """
        res = super().save()
        # Pass the workflow id so we have it for association.
        self._extract_concepts()
        if settings.NEO4J_ENABLED:
            self._establish_provenance()
        return res

    def _extract_concepts(self):
        pass

    def _establish_provenance(self):
        pass

    class Config:
        """
        Workflow Data Model Swagger Example
        """

        schema_extra = {"example": {}}
