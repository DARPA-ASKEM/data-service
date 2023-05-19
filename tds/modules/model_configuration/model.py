"""
TDS Model Configuration Data Model
"""
from typing import List, Optional

from pydantic import Field
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db.base import TdsModel
from tds.db.relational import engine as pg_engine
from tds.lib.concepts import mark_concept_active
from tds.settings import settings


class ModelConfiguration(TdsModel):
    name: str
    description: str
    index = "model_configuration"
    model_id: str
    model: object
    concepts: Optional[List] = []
    _exists = False

    def save(self, model_configuration_id: Optional[None | str | int] = None):
        if model_configuration_id is not None:
            self._exists = True
        res = super(ModelConfiguration, self).save(model_configuration_id)
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
        schema_extra = {"example": {"model_id": "unique_uuid", "configuration": {}}}

    @staticmethod
    def get_index():
        return "model_configuration"
