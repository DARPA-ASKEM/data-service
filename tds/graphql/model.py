"""
Model Schema
"""

# pylint: disable=missing-class-docstring, invalid-name, no-member, missing-function-docstring

from enum import Enum
from logging import Logger
from typing import List, Optional

import strawberry
from sqlalchemy.orm import Session
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import list_by_id
from tds.graphql.enum import ValueType
from tds.graphql.helper import MultipleOptionsError, fetch_by_curie, sqlalchemy_type
from tds.schema.model import ModelDescription

logger = Logger(__name__)


class ModelParameterSchema(schema.ModelParameter):
    class Config:
        orm_mode = True


class ModelFrameworkSchema(schema.ModelFramework):
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


@sqlalchemy_type(orm.ModelParameter)
@strawberry.experimental.pydantic.type(model=ModelFrameworkSchema)
class ModelFramework:
    name: strawberry.auto
    version: strawberry.auto
    semantics: strawberry.auto


def list_frameworks(info: Info) -> List[ModelParameter]:
    with Session(info.context["rdb"]) as session:
        frameworks: List[orm.ModelFramework] = session.query(orm.ModelFramework).all()
    return [ModelFramework.from_orm(framework) for framework in frameworks]


@sqlalchemy_type(orm.ModelDescription)
@strawberry.experimental.pydantic.type(model=ModelDescription)
class Model:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    framework_name: str
    timestamp: strawberry.auto
    state_id: strawberry.auto

    @strawberry.field
    def framework(self, info: Info) -> ModelFramework:
        with Session(info.context["rdb"]) as session:
            framework = session.query(orm.ModelFramework).get(self.framework_name)
            return ModelFramework.from_orm(framework)

    @strawberry.field
    def content(self, info: Info) -> str:
        with Session(info.context["rdb"]) as session:
            return str(session.query(orm.ModelState).get(self.state_id).content)

    @strawberry.field
    def parameters(self, info: Info) -> List[ModelParameter]:
        return list_parameters(self.id, info)

    @staticmethod
    def from_pydantic(instance: ModelDescription) -> "Model":
        data = instance.dict()
        data["framework_name"] = data.pop("framework")
        data.pop("concept")  # TODO: Include
        return Model(**data)


def list_models(
    info: Info, ids: Optional[List[int]] = None, curies: Optional[List[str]] = None
) -> List[Model]:

    if ids is not None and curies is not None:
        raise MultipleOptionsError

    if curies is not None:
        with Session(info.context["rdb"]) as session:
            return fetch_by_curie(session, Model, "models", curies)

    if ids is not None:
        with Session(info.context["rdb"]) as session:
            return Model.fetch_from_sql(session, ids)

    fetched_models: List[orm.ModelDescription] = list_by_id(
        info.context["rdb"].connect(), orm.ModelDescription, 100, 0
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


def list_intermediates(
    info: Info, ids: Optional[List[int]] = None, curies: Optional[List[str]] = None
) -> List[Intermediate]:
    if ids is not None and curies is not None:
        raise MultipleOptionsError

    if curies is not None:
        with Session(info.context["rdb"]) as session:
            return fetch_by_curie(session, Intermediate, "intermediates", curies)

    if ids is not None:
        with Session(info.context["rdb"]) as session:
            return Intermediate.fetch_from_sql(session, ids)

    fetched_intermediates: List[orm.Intermediate] = list_by_id(
        info.context["rdb"].connect(), orm.Intermediate, 100, 0
    )
    return [
        Intermediate.from_orm(intermediate) for intermediate in fetched_intermediates
    ]
