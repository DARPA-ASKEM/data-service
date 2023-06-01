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
    nodes: List = []

    _index = "workflow"

    def save(self):
        """
        Method saves the object to ElasticSearch.
        """
        res = super().save()
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

        schema_extra = {
            "example": {
                "name": "Test Workflow",
                "description": "This is the description",
                "nodes": [
                    {
                        "model": {
                            "id": "model_id",
                            "configurations": [{"id": "model_configuration_id"}],
                        }
                    }
                ],
            }
        }
