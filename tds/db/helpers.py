"""
Easy initialization and deletion of db content
"""
import json
from typing import Any

from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session

from tds.autogen import orm


def return_graph_validations():
    """
    read in graph relation file
    """
    with open("graph_relations.json", "r", encoding="utf-8") as file:
        validation = json.load(file)
    return validation


def return_graph_types():
    """
    return node types
    """
    validation = return_graph_validations()
    types = []
    for nodes in validation.get("relations").values():
        for node_pair in nodes:
            if node_pair[0] not in types:
                types.append(node_pair[0])
            if node_pair[1] not in types:
                types.append(node_pair[1])
    return types


def return_graph_relations():
    """
    return relations
    """
    validation = return_graph_validations()
    relations = []
    for relation in validation.get("relations").keys():
        if relation not in relations:
            relations.append(relation)
    return relations


def graph_abbreviations():
    """
    return abbreviations
    """
    validation = return_graph_validations()
    return validation.get("node_abbreviations")


def validate_relationship(left, right, relation_type):
    """
    validate a relationship for provenance
    """
    validations = return_graph_validations()
    relationship_allowed_types = validations.get("relations")[relation_type]
    for relation in relationship_allowed_types:
        if left == relation[0] and right == relation[1]:
            return True
    return False


def init_dev_content(connection: Connection):
    """
    Initialize tables in the connected DB
    """
    orm.Base.metadata.create_all(connection)


def drop_content(connection: Connection):
    """
    Drop all tables from the DB
    """
    return orm.Base.metadata.drop_all(connection)


def entry_exists(connection: Connection, orm_type: Any, id: int) -> bool:
    """
    Check if entry exists
    """
    with Session(connection) as session:
        return session.query(orm_type).filter(orm_type.id == id).count() == 1


def list_by_id(connection: Connection, orm_type: Any, page_size: int, page: int = 0):
    """
    Page through table using given ORM
    """
    with Session(connection) as session:
        return (
            session.query(orm_type)
            .order_by(orm_type.id.asc())
            .limit(page_size)
            .offset(page * page_size)
            .all()
        )
