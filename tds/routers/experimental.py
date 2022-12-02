"""
Experimental GraphQL router
"""

from logging import Logger
from typing import Any, Dict, List

import strawberry
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import list_by_id, request_rdb
from tds.schema import model
from tds.schema.project import ProjectMetadata

logger = Logger(__name__)


@strawberry.type
class Parameter:
    id: int
    name: str
    type: schema.ValueType
    default_value: str
    state_variable: bool


@strawberry.experimental.pydantic.type(model=model.Model)
class Model:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    framework: strawberry.auto
    timestamp: strawberry.auto
    content: str
    parameters: List[Parameter]

    @staticmethod
    def from_pydantic(instance: model.Model) -> "Model":
        data = instance.dict()
        data["content"] = str(data["content"])
        data.pop("concept")  # TODO: Include
        return Model(**data)


def list_models(info: Info) -> List["Model"]:
    fetched_models: List[orm.Model] = list_by_id(
        info.context["rdb"].connect(), orm.Model, 100, 0
    )
    to_graphql = lambda model: Model.from_pydantic(model.Model.from_orm(model))
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
