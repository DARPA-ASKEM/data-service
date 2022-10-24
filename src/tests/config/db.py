"""
config.db - The reusable DB connection
"""
# pylint: disable=attribute-defined-outside-init
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine, Connection
from main import init_dev_db_content


class TestAccessLayer:
    """
    Wrapper for generating an in-memory DB for running SQL-related tests
    """

    def __enter__(self) -> Engine:
        engine : Engine = create_engine('sqlite://')
        init_dev_db_content(engine)
        self.__connection : Connection = engine.connect()
        return engine

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.close()
