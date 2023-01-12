"""
Project Schema
"""

# pylint: disable=missing-class-docstring, no-member, missing-function-docstring

from logging import Logger
from typing import List, Optional

import strawberry
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import entry_exists, list_by_id
from tds.graphql.dataset import Dataset
from tds.graphql.helper import MultipleOptionsError, fetch_by_curie, sqlalchemy_type
from tds.graphql.model import Intermediate, Model
from tds.graphql.publication import Publication
from tds.graphql.simulation import Plan, Run
from tds.schema.project import ProjectMetadata
from tds.schema.resource import get_resource_orm

logger = Logger(__name__)


orm_enum_to_type = {
    orm.ResourceType.plans: Plan,
    orm.ResourceType.models: Model,
    orm.ResourceType.simulation_runs: Run,
    orm.ResourceType.datasets: Dataset,
    orm.ResourceType.intermediates: Intermediate,
    orm.ResourceType.publications: Publication,
}


def get_orm_from_alt_enum(type):
    return get_resource_orm(schema.ResourceType(type.name))


Asset = Model | Plan | Run | Dataset | Intermediate | Publication


def list_assets(project_id: int, info: Info) -> List[Asset]:
    if entry_exists(info.context["rdb"].connect(), orm.Project, project_id):
        with Session(info.context["rdb"]) as session:
            assets_xref: List[orm.ProjectAsset] = (
                session.query(orm.ProjectAsset)
                .filter(orm.ProjectAsset.project_id == project_id)
                .all()
            )

            assets = [
                orm_enum_to_type[entry.resource_type].fetch_from_sql(
                    session, entry.resource_id
                )
                for entry in assets_xref
            ]

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return assets


@sqlalchemy_type(orm.Project)
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


def list_projects(
    info: Info, ids: Optional[List[int]] = None, curies: Optional[List[int]] = None
) -> List[Project]:
    if ids is not None and curies is not None:
        raise MultipleOptionsError

    if curies is not None:
        with Session(info.context["rdb"]) as session:
            return fetch_by_curie(session, Project, "projects", curies)

    if ids is not None:
        with Session(info.context["rdb"]) as session:
            return Project.fetch_from_sql(session, ids)

    fetched_projects: List[orm.Project] = list_by_id(
        info.context["rdb"].connect(), orm.Project, 100, 0
    )
    return [Project.from_orm(proj) for proj in fetched_projects]
