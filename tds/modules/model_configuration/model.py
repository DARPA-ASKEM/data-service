"""
TDS Model Configuration Data Model
"""
from typing import List, Optional

from tds.db.base import TdsModel
from tds.settings import settings


class ModelConfiguration(TdsModel):
    """
    TDS Model Configuration Data Model.
    """

    name: str
    description: str
    _index = "model_configuration"
    model_id: str
    model: object
    concepts: Optional[List] = []
    exists: Optional[bool] = False

    def save(self, model_configuration_id: Optional[None | str | int] = None):
        if model_configuration_id is not None:
            self.exists = True
        res = super().save()
        # Pass the model_configuration id so we have it for association.
        self._extract_concepts(res["_id"])
        if settings.NEO4J_ENABLED:
            self._establish_provenance()
        return res

    def _extract_concepts(self, model_configuration_id):
        pass

    def _establish_provenance(self):
        pass

    class Config:
        """
        Config class for ModelConfiguration
        """

        schema_extra = {"example": {"model_id": "unique_uuid", "configuration": {}}}
