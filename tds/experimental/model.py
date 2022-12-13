"""
Model Schema
"""

from enum import Enum
from logging import Logger
from typing import List

import strawberry
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import entry_exists, list_by_id
from tds.experimental.enum import ValueType
from tds.experimental.helper import sqlalchemy_type
from tds.schema.model import ModelDescription

logger = Logger(__name__)


class ModelParameterSchema(schema.ModelParameter):
    class Config:
        orm_mode = True


@sqlalchemy_type(orm.ModelParameter)
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
    with Session(info.context["rdb"]) as session:
        parameters: List[orm.ModelParameter] = (
            session.query(orm.ModelParameter)
            .filter(orm.ModelParameter.model_id == model_id)
            .all()
        )
    return [ModelParameter.from_orm(param) for param in parameters]


@sqlalchemy_type(orm.Model)
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
    return [Model.from_orm(model) for model in fetched_models]


class IntermediateSchema(schema.Intermediate):
    class Config:
        orm_mode = True


@strawberry.enum
class IntermediateSource(Enum):

    mrepresentationa = schema.IntermediateSource.mrepresentationa.name
    skema = schema.IntermediateSource.skema.name


@strawberry.enum
class IntermediateFormat(Enum):
    bilayer = schema.IntermediateFormat.bilayer.name
    gromet = schema.IntermediateFormat.gromet.name
    sbml = schema.IntermediateFormat.sbml.name
    other = schema.IntermediateFormat.other.name


@sqlalchemy_type(orm.Intermediate)
@strawberry.experimental.pydantic.type(model=IntermediateSchema)
class Intermediate:
    id: strawberry.auto
    timestamp: strawberry.auto
    source: IntermediateSource
    type: IntermediateFormat
    content: str

    @staticmethod
    def from_pydantic(instance: IntermediateSchema) -> "Intermediate":
        data = instance.dict()
        data["type"] = IntermediateFormat(data["type"].name)
        data["source"] = IntermediateSource(data["source"].name)
        data["content"] = str(data["content"])
        return Intermediate(**data)


def list_intermediates(info: Info) -> List[Intermediate]:
    fetched_intermediates: List[orm.Intermediate] = list_by_id(
        info.context["rdb"].connect(), orm.Model, 100, 0
    )
    return [
        Intermediate.from_orm(intermediate) for intermediate in fetched_intermediates
    ]
