"""
Handler for object relations
"""

from typing import Optional

from fastapi import HTTPException
from neo4j import Driver
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.modules.provenance.model import Provenance, ProvenancePayload
from tds.modules.provenance.utils import validate_relationship


class ProvenanceHandler:
    """
    The handler wraps crud operations and writes to
    both the relational and graph DBs
    """

    def __init__(self, rdb: Engine, graph_db: Optional[Driver] = None):
        self.__connection__ = rdb.connect()
        self.graph_db = graph_db

    def cache_enabled(self):
        """
        Check if graph cache should be written to
        """
        return self.graph_db is not None

    def create_entry(self, entry: ProvenancePayload) -> int:
        """
        Draws a relation between two resources
        """
        # validate entry
        entry_dict = entry.dict()
        if not validate_relationship(
            left=entry_dict.get("left_type"),
            right=entry_dict.get("right_type"),
            relation_type=entry_dict.get("relation_type"),
        ):
            raise HTTPException(status_code=400, detail="Relationship not supported")

        with Session(self.__connection__) as session:
            provenance = Provenance(**entry_dict)
            session.add(provenance)
            session.commit()
            provenance_id: int = provenance.id

        if self.cache_enabled():
            self.create_node_relationship(entry_dict)

        return provenance_id

    # def create(self, left: Resource, right: Resource, label: RelationType) -> int:
    #     """
    #     Draws a relation between two resources
    #     """
    #     left_type = get_resource_type(left)
    #     right_type = get_resource_type(right)
    #     if left_type is not None and right_type is not None:
    #         entry = Provenance(
    #             left=left.id,
    #             left_type=left_type,
    #             right=right.id,
    #             right_type=right_type,
    #             relation_type=label,
    #             user_id=None,
    #         )
    #         id = self.create_entry(entry)

    #         return id
    #     raise Exception("Invalid object in relation")

    # def retrieve(self, id: int) -> Optional[Provenance]:
    #     """
    #     Retrieves a relation between two resources
    #     """
    #     with Session(self.__connection__) as session:
    #         if (
    #             session.query(orm.Provenance).filter(orm.Provenance.id == id).count()
    #             == 1
    #         ):
    #             provenance = session.query(orm.Provenance).get(id)
    #             return Provenance.from_orm(provenance)
    #         return None

    def delete(self, id: int) -> bool:
        """
        Deletes the edge between two resources (not the nodes)
        """
        with Session(self.__connection__) as session:
            if session.query(Provenance).filter(Provenance.id == id).count() == 1:
                provenance = session.query(Provenance).get(id)
                session.delete(provenance)
                session.commit()
                provenance_dict = provenance.__dict__

                if self.cache_enabled():
                    self.delete_node_relationship(provenance_payload=provenance_dict)

                return True

            return False

    def create_node_relationship(self, provenance_payload):
        """
        Create edge between two nodes
        """
        with self.graph_db.session() as session:
            # if node 1 is not created yet create node

            left_node_query = (
                f"Merge (n: {provenance_payload.get('left_type')}"
                + f"{{id: '{provenance_payload.get('left')}' , "
                + f"concept:'{provenance_payload.get('concept','.')}'}} )"
            )

            session.run(left_node_query)

            # if node 2 is not created yet create node

            right_node_query = (
                f"Merge (n: {provenance_payload.get('right_type')}"
                + f"{{id: '{provenance_payload.get('right')}' , concept:'.'}} )"
            )

            session.run(right_node_query)

            def user_id_str(user_id):
                if user_id is not None:
                    return " { user_id: $user_id}"
                return ""

            edge_query = (
                f"Match (n1: {provenance_payload.get('left_type')} ) "
                + "Where n1.id = $left_id "
                + f"Match (n2: {provenance_payload.get('right_type')} ) "
                + "Where n2.id = $right_id "
                + "Merge (n1)-[:"
                + provenance_payload.get("relation_type")
                + user_id_str(provenance_payload.get("user_id"))
                + "]->(n2)"
            )

            session.run(
                edge_query,
                left_id=provenance_payload.get("left"),
                right_id=provenance_payload.get("right"),
                user_id=provenance_payload.get("user_id", None),
            )

    def delete_node_relationship(self, provenance_payload):
        """
        Delete edge between two nodes
        """
        with self.graph_db.session() as session:
            query = (
                f"Match (n1: {provenance_payload.get('left_type')} ) "
                + "Where n1.id = $left "
                + f"Match (n2: {provenance_payload.get('right_type')} ) "
                + "Where n2.id = $right "
                + "Match (n1)-[r:"
                + provenance_payload.get("relation_type")
                # + " {user_id : $user_id}"
                + "]->(n2)"
                + "Delete r"
            )

            session.run(
                query,
                left=provenance_payload.get("left"),
                right=provenance_payload.get("right"),
                user_id=provenance_payload.get("user_id"),
            )

    def delete_nodes(self):
        """
        Prune nodes without edges
        """
        with self.graph_db.session() as session:
            query = "match (n) where not (n)--() delete (n)"
            session.run(query)
        return True

    def add_properties(self):
        """
        Modify properties so Neoviz can be used
        """
        with self.graph_db.session() as session:
            query = (
                "match (n)-[r]->(m)"
                + "SET n.name= labels(n)[0]"
                + "SET m.name= labels(m)[0]"
                + "SET r.name =type(r)"
                + "return *"
            )

            session.run(query)
            return True
