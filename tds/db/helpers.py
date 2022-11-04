"""
tds.db.helpers - Easy initialization and deletion of db content
"""
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session

from tds.autogen import orm


def init_dev_content(connection: Connection):
    """
    Initialize tables in the connected DB
    """
    orm.Base.metadata.create_all(connection)
    with Session(connection) as session:
        need_framework = session.query(orm.ModelingFramework).first() is None
        if need_framework:
            framework = orm.ModelingFramework(
                id=0,
                version="dummy",
                name="dummy",
                semantics={},
            )
            session.add(framework)
        session.commit()


def drop_content(connection: Connection):
    """
    Drop all tables from the DB
    """
    return orm.Base.metadata.drop_all(connection)
