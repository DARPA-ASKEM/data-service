"""
Experimental GraphQL router
"""

from enum import Enum
from logging import Logger
from typing import Any, Dict, List

import strawberry
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import entry_exists, list_by_id, request_rdb
from tds.schema.model import ModelDescription
from tds.schema.model import ModelParameter as ModelParameterSchema
from tds.schema.project import ProjectMetadata

logger = Logger(__name__)


@strawberry.enum
class ValueType(Enum):
    binary = schema.ValueType.binary.name
    bool = schema.ValueType.bool.name
    float = schema.ValueType.float.name
    int = schema.ValueType.int.name
    str = schema.ValueType.str.name


@strawberry.experimental.pydantic.type(model=ModelParameterSchema)
class ModelParameter:
    id: strawberry.auto
    name: strawberry.auto
    type: ValueType
    default_value: strawberry.auto
    state_variable: strawberry.auto

    @staticmethod
    def from_pydantic(instance: ModelParameterSchema) -> "ModelParameter":
        data = instance.dict()
        data["type"] = ValueType(data["type"].name)
        data.pop("model_id")
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


@strawberry.experimental.pydantic.type(model=ProjectMetadata)
class Project:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    timestamp: strawberry.auto
    active: strawberry.auto


def list_projects(info: Info) -> List[Project]:
    fetched_projects: List[orm.Project] = list_by_id(
        info.context["rdb"].connect(), orm.Project, 100, 0
    )
    to_graphql = lambda model: Project.from_pydantic(ProjectMetadata.from_orm(model))
    return [to_graphql(proj) for proj in fetched_projects]


def list_assets(root: Project, info: Info) -> None:
    pass


@strawberry.type
class Query:
    projects: List[Project] = strawberry.field(resolver=list_projects)
    models: List[Model] = strawberry.field(resolver=list_models)


schema = strawberry.Schema(query=Query)


async def get_context(
    rdb=Depends(request_rdb),
):
    return {
        "rdb": rdb,
    }


router = GraphQLRouter(schema, context_getter=get_context)
