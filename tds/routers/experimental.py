"""
Experimental GraphQL router
"""

from logging import Logger
from typing import List

import strawberry
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter

from tds.autogen import schema
from tds.db import request_rdb
from tds.experimental.model import Model, list_models
from tds.experimental.project import Project, list_projects
from tds.experimental.simulation import Run, list_runs

logger = Logger(__name__)


@strawberry.type
class Query:
    projects: List[Project] = strawberry.field(resolver=list_projects)
    models: List[Model] = strawberry.field(resolver=list_models)
    runs: List[Run] = strawberry.field(resolver=list_runs)


schema = strawberry.Schema(query=Query)


async def get_context(
    rdb=Depends(request_rdb),
):
    return {
        "rdb": rdb,
    }


router = GraphQLRouter(schema, context_getter=get_context)
