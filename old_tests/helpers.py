"""
The reusable Test DB connection
"""
import os
from contextlib import contextmanager
from sqlite3 import connect
from typing import Generator, Tuple

from fastapi.testclient import TestClient

# from neo4j import GraphDatabase
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from tds.db import init_dev_content, request_graph_db, request_rdb
from tds.server.build import build_api

# from tds.settings import settings

# rdb_engine = create_engine(
#     "sqlite:///.sqlite",
#     creator=lambda: connect(
#         "file:.sqlite",
#         uri=True,
#         check_same_thread=False,
#     ),
# )


# def demo_rdb_engine():
#     """
#     Provides postgres engine that can be used by FastAPI Dependencies
#     """
#     return rdb_engine


# NEO_ENGINE = GraphDatabase.driver(
#     "neo4j://localhost:7687", auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
# )


# def demo_neo_engine():
#     """
#     Provides graph driver that can be used by FastAPI Dependencies
#     """
#     return NEO_ENGINE


@contextmanager
def demo_rdb() -> Generator[Engine, None, None]:
    """
    Wraps for generating an in-memory DB for running SQL-related tests
    """

    if os.path.exists(".sqlite"):
        os.remove(".sqlite")

    engine = create_engine(
        "sqlite:///.sqlite",
        creator=lambda: connect(
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

        async def request_test_graph():
            yield None

        api.dependency_overrides[request_rdb] = request_test_rdb
        api.dependency_overrides[request_graph_db] = request_test_graph
        yield TestClient(api)


@contextmanager
def demo_api_context(
    *router_name: str,
) -> Generator[Tuple[TestClient, Engine], None, None]:
    """
    Environment for testing a router
    """
    api = build_api(*router_name)
    rdb = create_engine(
        "sqlite:///.sqlite",
        creator=lambda: connect(
            "file:.sqlite",
            uri=True,
            check_same_thread=False,
        ),
    )
    connection = rdb.connect()
    init_dev_content(connection)

    async def request_test_rdb():
        yield rdb

    async def request_test_graph():
        yield None

    api.dependency_overrides[request_rdb] = request_test_rdb
    api.dependency_overrides[request_graph_db] = request_test_graph
    try:
        yield (TestClient(api), rdb)
    finally:
        connection.close()
        os.remove(".sqlite")
