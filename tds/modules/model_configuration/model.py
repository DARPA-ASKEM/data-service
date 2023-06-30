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
    configuration: object
    amr_configuration: Optional[object]
    calibrated: Optional[bool] = False
    calibration: Optional[object]
    calibration_score: Optional[float]
    concepts: Optional[List] = []
    exists: Optional[bool] = False

    def save(self):
        res = super().save()
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

        schema_extra = {
            "example": {
                "model_id": "Model ID",
                "name": "Name",
                "description": "Description",
                "timestamp": "2023-01-01 00:00:00",
                "model_version": "1.0",
                "calibrated": True,
                "calibration_score": 1.047,
                "calibration": {"dataset_id": "covid-19-us-data"},
                "configuration": {},
            }
        }
