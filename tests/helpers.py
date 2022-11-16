"""
The reusable Test DB connection
"""
import os
from contextlib import contextmanager
from sqlite3 import connect
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from tds.db import init_dev_content, request_rdb
from tds.server.build import build_api


@contextmanager
def demo_rdb() -> Generator[Engine, None, None]:
    """
    Wraps for generating an in-memory DB for running SQL-related tests
    """

    engine = create_engine(
        "sqlite:///.sqlite",
        creator=lambda: connect(
            # "file:test:?mode=memory&cache=shared", uri=True, check_same_thread=False
            "file:.sqlite",
            uri=True,
            check_same_thread=False,
        ),
    )
    connection = engine.connect()
    init_dev_content(connection)
    try:
        yield engine
    finally:
        connection.close()
        os.remove(".sqlite")


@contextmanager
def demo_api(*router_name: str) -> Generator[TestClient, None, None]:
    """
    Environment for testing a router
    """
    api = build_api(*router_name)
    with demo_rdb() as rdb:

        async def request_test_rdb():
            yield rdb

        api.dependency_overrides[request_rdb] = request_test_rdb
        yield TestClient(api)
