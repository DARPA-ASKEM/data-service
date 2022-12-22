"""
Validate unit tests
"""

from dbml_builder import get_dbml_version
from fastapi.testclient import TestClient

from tds.autogen.schema import (
    IntermediateFormat,
    IntermediateSource,
    RelationType,
    ResourceType,
)
from tds.db import ProvenanceHandler
from tds.schema.resource import Intermediate, Publication, get_resource_type
from tds.server.build import build_api
from tds.settings import settings
from tests.helpers import demo_rdb


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
    with demo_rdb() as rdb:
        relation_handler = ProvenanceHandler(rdb, None)
        intermediate = Intermediate(
            id=0,
            source=IntermediateSource.skema,
            type=IntermediateFormat.other,
            content=b"",
        )
        publication = Publication(id=0, xdd_uri="https://", title="title")

        # NOTE: Should these two asserts be their own test?
        assert get_resource_type(intermediate) == ResourceType.intermediates
        assert get_resource_type(publication) == ResourceType.publications

        id = relation_handler.create(
            intermediate, publication, RelationType.derivedfrom
        )
        assert relation_handler.retrieve(id) is not None
        assert relation_handler.delete(id)
        assert relation_handler.retrieve(id) is None
