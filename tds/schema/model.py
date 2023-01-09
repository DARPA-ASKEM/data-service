"""
Provides the API interface for models.

Change to force rebuild.
"""
# pylint: disable=missing-class-docstring
from json import dumps
from typing import Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import Json

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
            "state_variable": param.state_variable,
        }
        for param in parameters
    ]


class ModelDescription(schema.ModelDescription):
    concept: Optional[Concept] = None

    class Config:
        orm_mode = True


class ModelOptPayload(schema.ModelDescription):
    left: int
    right: Optional[int]
    concept: Optional[Concept] = None
    parameters: Optional[ModelParameters] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "left": 1,
                "right": None,
                "name": "New model",
                "description": "Copy model 1 to New model",
                "content": "json-as-string",
                "parameters": [
                    {
                        "name": "param_1",
                        "type": "int",
                        "default_value": "1",
                        "state_variable": True,
                    }
                ],
                "framework": "string",
            }
        }


class ModelContent(schema.ModelState):
    @classmethod
    def from_orm(cls, body: orm.ModelState) -> "ModelContent":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        body.__dict__["content"] = dumps(body.content)

        return super().from_orm(body)

    class Config:
        orm_mode = True


class Model(schema.ModelDescription):
    concept: Optional[Concept] = None
    parameters: ModelParameters = []
    content: Json

    @classmethod
    def from_orm(
        cls,
        body: orm.ModelDescription,
        state: orm.ModelState,
        parameters: List[orm.ModelParameter],
    ) -> "Model":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        body.__dict__["content"] = dumps(ModelContent.from_orm(state).content)
        body.__dict__["parameters"] = orm_to_params(parameters)
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
                "state_variable": "bool",
            }
        }


class ModelFramework(schema.ModelFramework):
    class Config:
        orm_mode = True


class Intermediate(schema.Intermediate):
    class Config:
        orm_mode = True
