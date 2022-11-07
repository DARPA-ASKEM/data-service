"""
tds.schema.model - Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from json import dumps
from typing import Optional

from tds.autogen import orm, schema
from tds.schema.concept import Concept


class Model(schema.Model):
    concept: Optional[Concept]
    framework_id = 0  # TODO: Implement framework endpoints

    @classmethod
    def from_orm(cls, body: orm.Model) -> "Model":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        setattr(body, "content", dumps(body.content))
        return super().from_orm(body)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "Lorem ipsum dolor sit amet.",
                "content": "[]",
            }
        }
