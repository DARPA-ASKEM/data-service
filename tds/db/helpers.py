"""
Easy initialization and deletion of db content
"""
from typing import Any

from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session

from tds.autogen import orm


def init_dev_content(connection: Connection):
    """
    Initialize tables in the connected DB
    """
    orm.Base.metadata.create_all(connection)
    with Session(connection) as session:
        need_framework = session.query(orm.ModelFramework).first() is None
        if need_framework:
            framework = orm.ModelFramework(
                name="dummy",
                version="dummy",
                semantics="dummy",
            )
            session.add(framework)
        session.commit()


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
