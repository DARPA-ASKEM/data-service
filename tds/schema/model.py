"""
schema.dataset - Provides the API interface for datasets.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from json import dumps
from typing import Optional

from tds.autogen import orm, schema
from tds.schema.concept import Concept


class ModelBody(schema.Operation):
    framework_id = 0  # TODO(five): Implement framework crud
    # framework_name : str = 'dummy' # TODO(five): Look up id using name
    user = 0  # TODO(five): Implement person crud

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, body: orm.Operation) -> "ModelBody":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        setattr(body, "model_content", dumps(body.model_content))
        return super().from_orm(body)


class Model(schema.Model):
    body: ModelBody
    concept: Optional[Concept]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, metadata: orm.Model, body: orm.Operation) -> "Model":
        """
        Handle ORM conversion with insertion of model body into schema
        """
        model_body = ModelBody.from_orm(body)
        setattr(metadata, "body", model_body)
        return super().from_orm(metadata)
