"""
Initializes connection to Neo4j
"""

from neo4j import GraphDatabase

ENGINE = GraphDatabase.driver(
    "neo4j://graphdb.data-api:7687", auth=("neo4j", "password")
)


async def request_engine():
    """
    Provides graph driver that can be used by FastAPI Dependencies
    """
    return ENGINE
