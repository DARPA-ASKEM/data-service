"""
Experimental GraphQL router
"""

from logging import Logger
from typing import List

import strawberry
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session
from strawberry.fastapi import GraphQLRouter

from tds.autogen import orm
from tds.db import entry_exists, list_by_id, request_rdb
from tds.lib.simulations import adjust_run_params
from tds.operation import create, retrieve, update

logger = Logger(__name__)


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(query=Query)

router = GraphQLRouter(schema)
