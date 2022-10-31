"""
tests.utils - The reusable Test DB connection
"""
from contextlib import contextmanager
from sqlite3 import connect
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from src.main import build_api
from src.config.db import init_dev_content, drop_content


@contextmanager
def demo_engine() -> Generator[Engine, None, None]:
    """
    Wraps for generating an in-memory DB for running SQL-related tests
    """

    creator = lambda: connect("file:test:?mode=memory&cache=shared", uri=True)
    engine = create_engine('sqlite://', creator=creator)
    connection = engine.connect()
    init_dev_content(connection)
    try:
        yield engine
    except Exception as exception:
        raise exception
    finally:
        drop_content(connection)
        connection.close()


@contextmanager
def demo_api(router_name: str) -> Generator[TestClient, None, None]:
    """
    Environment for testing a router
    """
    context = demo_engine()
    try:
        yield TestClient(build_api(context.__enter__(), router_name))
    except Exception as exception:
        raise exception
    finally:
        context.__exit__(None, None, None)
