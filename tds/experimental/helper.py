"""
Strawberry helpers
"""

# from inspect import getargvalues, getfullargspec, currentframe
from logging import Logger
from typing import Any, List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from tds.autogen import orm, schema

logger = Logger(__name__)


class MultipleOptionsError(Exception):
    pass


def fetch_by_curie(
    session: Session,
    graphql_cls: Any,
    tag: schema.TaggableType | str,
    curies: List[str],
):
    if type(tag) is not schema.TaggableType:
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
    def add_sqlaclhemy_integration(graphql_cls):
        @staticmethod
        def from_orm(orm_obj: Any):
            if "_pydantic_type" not in dir(graphql_cls):
                raise TypeError("This schema does not inherit from a pydantic class")
            return graphql_cls.from_pydantic(
                graphql_cls._pydantic_type.from_orm(orm_obj)
            )

        graphql_cls.from_orm = from_orm
        graphql_cls.orm_cls = orm_cls

        @staticmethod
        def fetch_from_sql(session: Session, id: int | List[int]):
            if type(id) is int:
                return graphql_cls.from_orm(session.query(orm_cls).get(id))

            results = session.query(orm_cls).filter(orm_cls.id.in_(id)).all()
            return [graphql_cls.from_orm(result) for result in results]

        graphql_cls.fetch_from_sql = fetch_from_sql

        """
        filterable_fields = [ k for k,v in graphql_cls.__dataclass_fields__.items() if v.compare]
        field_types = { k: Optional[graphql_cls.__annotations__[k]] for k in filterable_fields }

        @staticmethod
        def sql_search(info: Info):
            filters = []
            kwargs = getargvalues(currentframe())[3]
            for field_name, filter_value in kwargs.items():
                if field_name not in filterable_fields or filter_value is None:
                    continue
                else:
                    filters.append(getattr(orm, field_name) == filter_value)
                    
            with Session(info.context["rdb"]) as session:
                sql_results = session.query(orm).filter(*filters).all()
            return [ orm_to_graphql(graphql_cls, entry) for entry in sql_results ]
        sql_search.__annotations__.update(field_types)
        src = sql_search.__code__
        sql_search.__code__.replace(
            co_argcount=len(field_types) + src.co_argcount,
            co_varnames=src.co_varnames + tuple(filterable_fields),
        )
        sql_search.__defaults__ = (None,) * len(field_types)
        graphql_cls.sql_search = sql_search
        """

        return graphql_cls

    return add_sqlaclhemy_integration
