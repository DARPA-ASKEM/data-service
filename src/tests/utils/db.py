"""
config.db - The reusable DB connection
"""
from contextlib import contextmanager
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from main import build_api, init_dev_db_content


@contextmanager
def demo_engine() -> Generator[Engine, None, None]:
    """
    Wraps for generating an in-memory DB for running SQL-related tests
    """
    engine = create_engine('sqlite://')
    connection = engine.connect()
    init_dev_db_content(connection)
    try:
        yield engine
    finally:
        connection.close()


@contextmanager
def demo_api(router_name: str) -> Generator[TestClient, None, None]:
    """
    Environment for testing a router
    """
    try:
        with demo_engine() as engine:
            yield TestClient(build_api(engine, router_name))
    finally:
        pass
