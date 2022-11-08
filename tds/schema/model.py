"""
tds.schema.model - Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from json import dumps
from typing import Dict, List, Optional

from pydantic import BaseModel

from tds.autogen import orm, schema
from tds.schema.concept import Concept


class Parameter(BaseModel):
    name: str
    type: schema.ValueType

    class Config:
        orm_mode = True


class Model(schema.Model):
    concept: Optional[Concept]
    framework_id = 0  # TODO: Implement framework endpoints
    parameters: Dict[str, schema.ValueType] = {}

    @classmethod
    def from_orm(cls, body: orm.Model, parameters: List[orm.ModelParameter]) -> "Model":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        setattr(body, "content", dumps(body.content))
        setattr(body, "parameters", {param.name: param.type for param in parameters})
        return super().from_orm(body)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "Lorem ipsum dolor sit amet.",
                "content": "[]",
                "parameters": {"x": "int"},
            }
        }
