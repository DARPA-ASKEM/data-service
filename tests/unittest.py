"""
Validate unit tests
"""

from dbml_builder import get_dbml_version

# from fastapi import Depends
from fastapi.testclient import TestClient

from tds.autogen.schema import RelationType
from tds.db import ProvenanceHandler
from tds.server.build import build_api
from tds.settings import settings
from tests.helpers import demo_neo_engine, demo_rdb_engine


def test_version() -> None:
    """
    Ensure the code is not using an outdated version of the DBML
    """
    assert settings.DBML_VERSION == get_dbml_version(settings.DBML_PATH)


def test_build_api() -> None:
    """
    Ensure that the API can be built
    """
    client = TestClient(build_api())
    response = client.get("/")
    assert response.status_code == 200


def test_relation_handler_rdb_only():
    """
    Ensure the provenance handler can create a basic edge
    """
    graph_db = demo_neo_engine()
    rdb = demo_rdb_engine()
    relation_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
    provenance_payload = {
        "left": 1,
        "left_type": "Intermediate",
        "right": 2,
        "right_type": "Publication",
        "relation_type": RelationType.EXTRACTED_FROM,
        "user_id": 1,
    }

    relation_handler.create_node_relationship(provenance_payload=provenance_payload)
