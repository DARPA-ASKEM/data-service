"""
Strawberry helpers
"""

from typing import Any


def orm_to_graphql(graphql_class: Any, orm: Any):
    """
    Returns Strawberry object from ORM
    """
    return graphql_class.from_pydantic(graphql_class._pydantic_type.from_orm(orm))
