"""
Easy initialization and deletion of db content
"""
from typing import Any

from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session

from tds.db.base import Base


def init_dev_content(connection: Connection):
    """
    Initialize tables in the connected DB
    """
    Base.metadata.create_all(connection)


def drop_content(connection: Connection):
    """
    Drop all tables from the DB
    """
    return Base.metadata.drop_all(connection)


def entry_exists(connection: Connection, orm_type: Any, orm_id: int) -> bool:
    """
    Check if entry exists
    """
    with Session(connection) as session:
        return session.query(orm_type).filter(orm_type.id == orm_id).count() == 1


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
