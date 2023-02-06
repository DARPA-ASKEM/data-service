"""
Experimental GraphQL router
"""

from logging import Logger
from typing import List

import strawberry
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter

from tds.autogen import schema
from tds.db import request_graph_db, request_rdb
from tds.graphql.concept import Concept, list_concepts
from tds.graphql.dataset import Dataset, list_datasets
from tds.graphql.model import (
    Intermediate,
    Model,
    ModelFramework,
    list_frameworks,
    list_intermediates,
    list_models,
)
from tds.graphql.project import Project, list_projects
from tds.graphql.provenance import Provenance, list_nodes
from tds.graphql.publication import Publication, list_publications
from tds.graphql.simulation import Plan, Run, list_plans, list_runs

logger = Logger(__name__)


@strawberry.type
class Query:
    """
    Top level GraphQL retrieval query
    """

    projects: List[Project] = strawberry.field(resolver=list_projects)
    models: List[Model] = strawberry.field(resolver=list_models)
    runs: List[Run] = strawberry.field(resolver=list_runs)
    plans: List[Plan] = strawberry.field(resolver=list_plans)
    datasets: List[Dataset] = strawberry.field(resolver=list_datasets)
    concepts: List[Concept] = strawberry.field(resolver=list_concepts)
    provenance: List[Provenance] = strawberry.field(resolver=list_nodes)
    intermediates: List[Intermediate] = strawberry.field(resolver=list_intermediates)
    publications: List[Publication] = strawberry.field(resolver=list_publications)
    frameworks: List[ModelFramework] = strawberry.field(resolver=list_frameworks)


schema = strawberry.Schema(query=Query)


async def get_context(rdb=Depends(request_rdb), graph_db=Depends(request_graph_db)):
    """
    Provides FastAPI dependencies to GraphQL
    """
    return {"rdb": rdb, "graph_db": graph_db}


router = GraphQLRouter(schema, context_getter=get_context)
