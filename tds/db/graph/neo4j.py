"""
Initializes connection to Neo4j
"""

from neo4j import GraphDatabase

from tds.settings import settings

ENGINE = GraphDatabase.driver(
    settings.NEO4J_driver, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)


async def request_engine():
    """
    Provides graph driver that can be used by FastAPI Dependencies
    """
    return ENGINE
