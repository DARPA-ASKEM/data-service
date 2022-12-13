"""
Strawberry helpers
"""

from logging import Logger
from typing import Any, List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from tds.autogen import orm, schema

logger = Logger(__name__)


class MultipleOptionsError(Exception):
    """
    Error to throw when too many options are passed into a query
    """


def fetch_by_curie(
    session: Session,
    graphql_cls: Any,
    tag: schema.TaggableType | str,
    curies: List[str],
):
    """
    Return a given object that is attached to a concept in the list of curies
    """
    if isinstance(tag, schema.TaggableType):
        tag = schema.TaggableType(tag)
    results = (
        session.query(orm.OntologyConcept)
        .filter(orm.OntologyConcept.curie.in_(curies))
        .join(
            graphql_cls.orm_cls,
            and_(
                orm.OntologyConcept.type == tag,
                orm.OntologyConcept.object_id == graphql_cls.orm_cls.id,
            ),
        )
        .with_entities(graphql_cls.orm_cls)
        .all()
    )
    return [graphql_cls.from_orm(result) for result in results]


def sqlalchemy_type(orm_cls: Any):
    """
    Generate a class wrapper
    """

    def add_sqlaclhemy_integration(graphql_cls):
        """
        Add SQLAlchemy integration to strawberry
        """

        @staticmethod
        def from_orm(orm_obj: Any):
            """
            Convert from ORM to strawberry type
            """
            if "_pydantic_type" not in dir(graphql_cls):
                raise TypeError("This schema does not inherit from a pydantic class")
            return graphql_cls.from_pydantic(
                graphql_cls._pydantic_type.from_orm(
                    orm_obj
                )  # pylint: disable=protected-access
            )

        graphql_cls.from_orm = from_orm
        graphql_cls.orm_cls = orm_cls

        @staticmethod
        def fetch_from_sql(session: Session, id: int | List[int]):
            """
            Fetch strawberry type from sql
            """
            if isinstance(id, int):
                return graphql_cls.from_orm(session.query(orm_cls).get(id))

            results = session.query(orm_cls).filter(orm_cls.id.in_(id)).all()
            return [graphql_cls.from_orm(result) for result in results]

        graphql_cls.fetch_from_sql = fetch_from_sql

        return graphql_cls

    return add_sqlaclhemy_integration
