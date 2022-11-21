"""
The configured DB engine
"""

from neo4j import GraphDatabase
from sqlalchemy import create_engine

from tds.settings import settings

neo_engine = GraphDatabase.driver(
    "neo4j://graphdb.data-api:7687", auth=("neo4j", "password")
)

# pylint: disable-next=line-too-long
url = f"postgresql://{settings.SQL_USER}:{settings.SQL_PASSWORD}@{settings.SQL_URL}:{settings.SQL_PORT}/askem"
engine = create_engine(url, connect_args={"connect_timeout": 8})


async def request_engine():
    """
    Provides postgres engine that can be used by FastAPI Dependencies
    """
    return engine


async def request_graph_engine():
    """
    Provides neo4j engine that can be used by FastAPI Dependencies
    """
    return neo_engine
