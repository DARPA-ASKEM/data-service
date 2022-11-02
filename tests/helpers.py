"""
tests.utils - The reusable Test DB connection
"""
from contextlib import contextmanager
from sqlite3 import connect
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from tds.db import drop_content, init_dev_content
from tds.server.build import build_api


@contextmanager
def demo_engine() -> Generator[Engine, None, None]:
    """
    Wraps for generating an in-memory DB for running SQL-related tests
    """

    engine = create_engine(
        "sqlite://",
        creator=lambda: connect("file:test:?mode=memory&cache=shared", uri=True),
    )
    connection = engine.connect()
    init_dev_content(connection)
    try:
        yield engine
    finally:
        drop_content(connection)
        connection.close()


@contextmanager
def demo_api(router_name: str) -> Generator[TestClient, None, None]:
    """
    Environment for testing a router
    """
    # pylint: disable=no-member
    context = demo_engine()
    try:
        yield TestClient(build_api(context.__enter__(), router_name))
    finally:
        context.__exit__(None, None, None)
