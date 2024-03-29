"""
TDS Model Configuration Response object.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ModelConfigurationResponse(BaseModel):
    """
    Model Configuration Response Object.
    """

    id: str
    name: str
    description: str
    timestamp: datetime
    model_id: str
    configuration: object
    amr_configuration: object
    calibrated: Optional[bool]
    calibration: Optional[object]
    calibration_score: Optional[float]
    model_id: str


def configuration_response(model_configuration_list):
    """
    Function builds list of model configs for response.
    """
    return [
        ModelConfigurationResponse(**x["_source"]) for x in model_configuration_list
    ]
