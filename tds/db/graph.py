"""
Handler for object relations
"""

from typing import Optional

from fastapi import Depends
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.autogen.schema import RelationType
from tds.db.relational import request_engine as request_rdb
from tds.db.relational import request_graph_engine
from tds.schema.provenance import Provenance
from tds.schema.resource import ResourceType


class ProvenanceHandler:
    """
    The handler wraps crud operations and writes to both the relational and graph DBs
    """

    def __init__(self, rdb: Engine, neo_engine, enable_graph_cache: bool = True):
        self.__connection__ = rdb.connect()
        self.graph_cache_enabled = enable_graph_cache
        self.neo_engine = neo_engine

    def create(
        self,
        left: int,
        left_type: ResourceType,
        right: int,
        right_type: ResourceType,
        relation_type: RelationType,
        user_id: int,
    ) -> dict:
        """
        Draws a relation between two resources
        """

        if left_type is not None and right_type is not None:
            provenance_schema = Provenance(
                left=left,
                left_type=left_type,
                right=right,
                right_type=right_type,
                relation_type=relation_type,
                user_id=user_id,
            )
            provenance_payload = provenance_schema.dict()
            with Session(self.__connection__) as session:
                provenance = orm.Provenance(**provenance_payload)
                session.add(provenance)
                session.commit()
                id: int = provenance.id

            if self.graph_cache_enabled:
                self.create_node_relationship(provenance_payload=provenance_payload)

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

    ## neo4j functions
    def create_node(self, id, label):
        with self.neo_engine.session() as session:
            query_label = f"{label.capitalize()}"
            results = session.run(
                "Create (n:" + query_label + ")" + "SET n.id = $id_", id_=id
            )
            print(results)

    def delete_node(self, id):
        with self.neo_engine.session() as session:
            # query_label = f"{label.capitalize()}"
            results = session.run(
                "Match (n) \
                Where n.id = $id_ \
                Delete n",
                id_=id,
            )
            print(results)

    def create_node_relationship(self, provenance_payload):
        with self.neo_engine.session() as session:

            # if node 1 is not created yet create node
            q = (
                f"Merge (n: {provenance_payload.get('left_type')}"
                + "{ id: $left_id } )"
            )
            print(q)
            session.run(q, left_id=provenance_payload.get("left"))

            # if node 2 is not created yet create node
            q = (
                f"Merge (n: {provenance_payload.get('right_type')}"
                + "{ id: $right_id } )"
            )
            print(q)
            session.run(q, right_id=provenance_payload.get("right"))

            # Match our two nodes and create new relationship. Set user_id as property of relationship
            q = (
                f"Match (n1: {provenance_payload.get('left_type')} ) "
                + "Where n1.id = $left_id "
                + f"Match (n2: {provenance_payload.get('right_type')} ) "
                + "Where n2.id = $right_id "
                + "Merge (n1)-[:"
                + provenance_payload.get("relation_type")
                + " {user_id : $user_id"
                + "}]->(n2)"
            )
            print(q)
            session.run(
                q,
                left_id=provenance_payload.get("left"),
                right_id=provenance_payload.get("right"),
                user_id=provenance_payload.get("user_id"),
            )

    def delete_node_relationship(self, node_1, node_2, relationship, user_id):
        with self.neo_engine.session() as session:
            q = (
                f"Match (n1: {node_1.get('label')} ) "
                + "Where n1.id = $node_1_id_ "
                + f"Match (n2: {node_2.get('label')} ) "
                + "Where n2.id = $node_2_id_ "
                + "Match (n1)-[r:"
                + relationship
                + " {user_id : $user_id"
                + "}]->(n2)"
                + "Delete r"
            )

            print(q)
            res = session.run(
                q,
                node_1_id_=node_1.get("id"),
                node_2_id_=node_2.get("id"),
                user_id=user_id,
            )
            print(res)

    def neo_close(self):
        self.neo_engine.close()


async def request_provenance_handler(
    rdb: Engine = Depends(request_rdb), neo_engine=Depends(request_graph_engine)
) -> ProvenanceHandler:
    """
    Create a fastapi dependency relational handler
    """
    return ProvenanceHandler(rdb, neo_engine=neo_engine)
