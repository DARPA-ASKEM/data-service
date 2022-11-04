"""
tds.relation.provenance - Handler for object relations
"""

from typing import Optional, Type

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.autogen.schema import RelationType
from tds.db import request_rdb
from tds.schema.provenance import Provenance
from tds.schema.resources import get_resource_type


class RelationHandler:
    """
    The handler wraps crud operations and writes to both the relational and graph DBs
    """

    def __init__(self, rdb, enable_graph_cache: bool = True):
        self.__connection__ = rdb.connect()
        self.graph_cache_enabled = enable_graph_cache  # TODO: create neo4j connection

    def create(
        self, left: Type[BaseModel], right: Type[BaseModel], label: RelationType
    ) -> int:
        """
        Draws a relation between two resources
        """
        left_type = get_resource_type(left)
        right_type = get_resource_type(right)
        if left_type is not None and right_type is not None:
            provenance_schema = Provenance(
                left=left.id,
                left_type=left_type,
                right=right.id,
                right_type=right_type,
                relation_type=label,
                user_id=None,
            )
            provenance_payload = provenance_schema.dict()
            with Session(self.__connection__) as session:
                provenance = orm.Provenance(**provenance_payload)
                session.add(provenance)
                session.commit()
                id: int = provenance.id
            return id
        raise Exception("Invalid object in relation")

    def retrieve(self, id: int) -> Optional[Provenance]:
        """
        Retrieves a relation between two resources
        """
        with Session(self.__connection__) as session:
            if (
                session.query(orm.Provenance).filter(orm.Provenance.id == id).count()
                == 1
            ):
                provenance = session.query(orm.Provenance).get(id)
                return Provenance.from_orm(provenance)
            return None

    def delete(self, id: int) -> bool:
        """
        Deletes the edge between two resources (not the nodes)
        """
        with Session(self.__connection__) as session:
            if (
                session.query(orm.Provenance).filter(orm.Provenance.id == id).count()
                == 1
            ):
                provenance = session.query(orm.Provenance).get(id)
                session.delete(provenance)
                session.commit()
                return True
            return False


async def request_relation_handler(
    rdb: Engine = Depends(request_rdb),
) -> RelationHandler:
    """
    Create a fastapi dependency relational handler
    """
    return RelationHandler(rdb)
