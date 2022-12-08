"""
Project Schema
"""

from logging import Logger
from typing import List

import strawberry
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import entry_exists, list_by_id
from tds.experimental.helper import orm_to_graphql
from tds.experimental.model import Model
from tds.experimental.simulation import Plan, Run
from tds.schema.project import ProjectMetadata
from tds.schema.resource import get_resource_orm

logger = Logger(__name__)


IMPLEMENTED_TYPES = [
    orm.ResourceType(type) for type in ["plans", "models", "simulation_runs"]
]

orm_enum_to_type = {
    orm.ResourceType.plans: Plan,
    orm.ResourceType.models: Model,
    orm.ResourceType.simulation_runs: Run,
}

get_orm_from_alt_enum = lambda type: get_resource_orm(schema.ResourceType(type.name))

Asset = Model | Plan | Run


def list_assets(project_id: int, info: Info) -> List[Asset]:
    if entry_exists(info.context["rdb"].connect(), orm.Project, project_id):
        with Session(info.context["rdb"]) as session:
            assets_xref: List[orm.ProjectAsset] = (
                session.query(orm.ProjectAsset)
                .filter(orm.ProjectAsset.project_id == project_id)
                .all()
            )

            assets = [
                orm_to_graphql(
                    orm_enum_to_type[entry.resource_type],
                    session.query(get_orm_from_alt_enum(entry.resource_type)).get(
                        entry.resource_id
                    ),
                )
                for entry in assets_xref
                if entry.resource_type in IMPLEMENTED_TYPES
            ]

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return assets


@strawberry.experimental.pydantic.type(model=ProjectMetadata)
class Project:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    timestamp: strawberry.auto
    active: strawberry.auto

    @strawberry.field
    def assets(self, info: Info) -> List[Asset]:
        return list_assets(self.id, info)


def list_projects(info: Info) -> List[Project]:
    fetched_projects: List[orm.Project] = list_by_id(
        info.context["rdb"].connect(), orm.Project, 100, 0
    )
    return [orm_to_graphql(Project, proj) for proj in fetched_projects]
