"""
src.db.helpers - Easy initialization and deletion of db content
"""
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session
from src.autogen import orm


def init_dev_content(connection: Connection):
    """
    Initialize tables in the connected DB
    """
    orm.Base.metadata.create_all(connection)
    with Session(connection) as session:
        need_framework = session.query(orm.Framework).first() is None
        need_person = session.query(orm.Person).first() is None
        if need_framework:
            framework = orm.Framework(
                id=0,
                version="dummy",
                name="dummy",
                semantics={},
            )
            session.add(framework)
        if need_person:
            person = orm.Person(
                id=0,
                name="Jane Doe",
                email="sample",
                org="sample",
                website="sample",
                is_registered=True,
            )
            session.add(person)
        session.commit()


def drop_content(connection: Connection):
    """
    Drop all tables from the DB
    """
    return orm.Base.metadata.drop_all(connection)
