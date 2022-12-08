"""
Strawberry helpers
"""

from logging import Logger
from typing import Any

logger = Logger(__name__)


def orm_to_graphql(graphql_class: Any, orm: Any):
    """
    Returns Strawberry object from ORM
    """
    return graphql_class.from_pydantic(graphql_class._pydantic_type.from_orm(orm))
