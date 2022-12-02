"""
Project Schema
"""

from logging import Logger
from typing import List

import strawberry
from strawberry.types import Info

from tds.autogen import orm
from tds.db import list_by_id
from tds.schema.project import ProjectMetadata

logger = Logger(__name__)


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
