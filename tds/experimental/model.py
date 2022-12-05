"""
Model Schema
"""

from logging import Logger
from typing import List

import strawberry
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import entry_exists, list_by_id
from tds.experimental.enum import ValueType
from tds.schema.model import ModelDescription

logger = Logger(__name__)


class ModelParameterSchema(schema.ModelParameter):
    class Config:
        orm_mode = True


@strawberry.experimental.pydantic.type(model=ModelParameterSchema)
class ModelParameter:
    id: strawberry.auto
    model_id: strawberry.auto
    name: strawberry.auto
    type: ValueType
    default_value: strawberry.auto
    state_variable: strawberry.auto

    @staticmethod
    def from_pydantic(instance: ModelParameterSchema) -> "ModelParameter":
        data = instance.dict()
        data["type"] = ValueType(data["type"].name)
        return ModelParameter(**data)


def list_parameters(model_id: int, info: Info) -> List[ModelParameter]:
    if entry_exists(info.context["rdb"].connect(), orm.Model, model_id):
        with Session(info.context["rdb"]) as session:
            parameters: List[orm.ModelParameter] = (
                session.query(orm.ModelParameter)
                .filter(orm.ModelParameter.model_id == model_id)
                .all()
            )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    to_graphql = lambda model: ModelParameter.from_pydantic(
        ModelParameterSchema.from_orm(model)
    )
    return [to_graphql(param) for param in parameters]


@strawberry.experimental.pydantic.type(model=ModelDescription)
class Model:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    framework: strawberry.auto
    timestamp: strawberry.auto
    content: str

    @strawberry.field
    def parameters(self, info: Info) -> List[ModelParameter]:
        return list_parameters(self.id, info)

    @staticmethod
    def from_pydantic(instance: ModelDescription) -> "Model":
        data = instance.dict()
        data["content"] = str(data["content"])
        data.pop("concept")  # TODO: Include
        return Model(**data)


def list_models(info: Info) -> List[Model]:
    fetched_models: List[orm.Model] = list_by_id(
        info.context["rdb"].connect(), orm.Model, 100, 0
    )
    to_graphql = lambda model: Model.from_pydantic(ModelDescription.from_orm(model))
    return [to_graphql(model) for model in fetched_models]
