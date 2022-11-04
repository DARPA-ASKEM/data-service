"""
tds.relation.provenance - Handler for object relations
"""

from typing import Optional, Type

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.autogen.schema import Provenance, RelationType
from tds.db import request_rdb
from tds.schema.resources import get_resource_type


class RelationHandler:
    """
    The hanlder wraps relation crud operations and writes to both the relational and graph DBs
    """

    def __init__(self, rdb, enable_graph_cache: bool = True):
        self.__connection__ = rdb.connect()
        self.graph_cache_enabled = enable_graph_cache  # TODO: create neo4j connection

    def create(
        self, left: Type[BaseModel], right: Type[BaseModel], label: RelationType
    ) -> int:
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
        else:
            raise Exception("Invalid object in relation")

    def retrieve(self, id: int) -> Optional[Provenance]:
        with Session(self.__connection__) as session:
            if session.query(orm.Provenance).filter(orm.Software.id == id).count() == 1:
                provenance = session.query(orm.Provenance).get(id)
                return Provenance.from_orm(provenance)
            else:
                return None

    def delete(self, id: int) -> bool:
        with Session(self.__connection__) as session:
            if session.query(orm.Provenance).filter(orm.Software.id == id).count() == 1:
                provenance = session.query(orm.Provenance).get(id)
                session.delete(provenance)
                session.commit()
                return True
            else:
                return False


async def request_relation_handler(
    rdb: Engine = Depends(request_rdb),
) -> RelationHandler:
    return RelationHandler(rdb)
