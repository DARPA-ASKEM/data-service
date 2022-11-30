"""
Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from json import dumps
from typing import Dict, List, Optional

from fastapi.encoders import jsonable_encoder

from tds.autogen import orm, schema
from tds.schema.concept import Concept

ModelParameters = List[Dict]


def orm_to_params(parameters: List[orm.ModelParameter]) -> ModelParameters:
    """
    Convert SQL parameter search to dict
    """
    return [
        {
            "id": param.id,
            "name": param.name,
            "type": jsonable_encoder(param.type),
            "default_value": param.default_value,
            "initial": param.initial,
        }
        for param in parameters
    ]


class ModelDescription(schema.Model):
    concept: Optional[Concept] = None

    class Config:
        orm_mode = True


class Model(schema.Model):
    concept: Optional[Concept] = None
    parameters: ModelParameters = []

    @classmethod
    def from_orm(cls, body: orm.Model, parameters: List[orm.ModelParameter]) -> "Model":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        setattr(body, "content", dumps(body.content))
        setattr(body, "parameters", orm_to_params(parameters))

        return super().from_orm(body)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "string",
                "description": "string",
                "content": "json-as-string",
                "parameters": [{"string": "value-type"}],
                "framework": "string",
                "initial": "bool",
            }
        }


class ModelFramework(schema.ModelFramework):
    class Config:
        orm_mode = True


class Intermediate(schema.Intermediate):
    class Config:
        orm_mode = True
