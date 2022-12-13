"""
Publication Schema
"""

# pylint: disable=missing-class-docstring, no-member, missing-function-docstring

from logging import Logger
from typing import List, Optional

import strawberry
from sqlalchemy.orm import Session
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import list_by_id
from tds.graphql.helper import MultipleOptionsError, fetch_by_curie, sqlalchemy_type

logger = Logger(__name__)


class PublicationSchema(schema.Publication):
    class Config:
        orm_mode = True


@sqlalchemy_type(orm.Publication)
@strawberry.experimental.pydantic.type(model=PublicationSchema)
class Publication:
    id: strawberry.auto
    xdd_uri: strawberry.auto
    title: strawberry.auto


def list_publications(
    info: Info, ids: Optional[List[int]] = None, curies: Optional[List[str]] = None
) -> List[Publication]:
    if ids is not None and curies is not None:
        raise MultipleOptionsError

    if curies is not None:
        with Session(info.context["rdb"]) as session:
            return fetch_by_curie(session, Publication, "publications", curies)
    if ids is not None:
        with Session(info.context["rdb"]) as session:
            return Publication.fetch_from_sql(session, ids)
    fetched_publications: List[orm.Publication] = list_by_id(
        info.context["rdb"].connect(), orm.Publication, 100, 0
    )
    return [Publication.from_orm(publication) for publication in fetched_publications]
