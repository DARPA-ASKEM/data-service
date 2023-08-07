"""
Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from typing import Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from tds.modules.model.model import ModelFrameworkPayload

ModelParameters = List[Dict]


def orm_to_params(parameters: List) -> ModelParameters:
    """
    Convert SQL parameter search to dict
    """
    return [
        {
            "id": param.id,
            "name": param.name,
            "type": jsonable_encoder(param.type),
            "default_value": param.default_value,
            "state_variable": param.state_variable,
        }
        for param in parameters
    ]


class ModelOptPayload(BaseModel):
    left: int
    right: Optional[int]
    name: str
    description: Optional[str]
    framework: str
    content: Optional[list] = None
    parameters: Optional[list] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "left": 1,
                "right": None,
                "name": "New model",
                "description": "Copy model 1 to New model",
                "content": {},
                "parameters": [
                    {
                        "name": "param_1",
                        "type": "int",
                        "default_value": "1",
                        "state_variable": True,
                    }
                ],
                "framework": "Petri Net",
            }
        }


class ModelFramework(ModelFrameworkPayload):
    class Config:
        orm_mode = True
