"""
TDS Code Data Model Definition.
"""
from typing import Any, List, Optional

from tds.db.base import TdsModel

# from tds.settings import settings


class Code(TdsModel):
    """
    Code Data Model
    """

    name: str
    description: str

    _index = "code"
    concepts: Optional[List] = []

    # def save(self):
    #     """
    #     Method saves the object to ElasticSearch.
    #     """
    #     res = super().save()
    #     # self._extract_concepts()
    #     if settings.NEO4J_ENABLED:
    #         self._establish_provenance()
    #     return res

    # def _extract_concepts(self, artifact_id):
    #     pass

    # def _establish_provenance(self):
    #     pass

    class Config:
        """
        Code Data Model Swagger Example
        """

        schema_extra = {"example": {}}
