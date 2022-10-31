"""
config.db - The reusable DB connection
"""
from sqlalchemy import create_engine
from sqlalchemy.engine.base import  Connection
from sqlalchemy.orm import Session
from src.config.settings import settings
from src.generated import orm

# pylint: disable-next=line-too-long
url = f'postgresql://{settings.sql_user}:{settings.sql_password}@{settings.sql_url}:{settings.sql_port}/askem'

engine = create_engine(url, connect_args={'connect_timeout':8})


def init_dev_content(connection : Connection):
    """
    Initialize tables in the connected DB
    """
    orm.Base.metadata.create_all(connection)
    with Session(connection) as session:
        need_framework = session.query(orm.Framework).first() is None
        need_person = session.query(orm.Person).first() is None
        if need_framework:
            framework = orm.Framework(
                id = 0,
                version = "dummy",
                name = "dummy",
                semantics = {},
            )
            session.add(framework)
        if need_person:
            person = orm.Person(
                id = 0,
                name = "Jane Doe",
                email = "sample",
                org = "sample",
                website = "sample",
                is_registered = True
            )
            session.add(person)
        session.commit()


drop_content = lambda connection: orm.Base.metadata.drop_all(connection)
