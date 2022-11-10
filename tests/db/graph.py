"""
tests.relation.provenance - Test provenance wrapper
"""
from tds.autogen.schema import (
    IntermediateFormat,
    IntermediateSource,
    RelationType,
    ResourceType,
)
from tds.db import ProvenanceHandler
from tds.schema.resources import Intermediate, Publication, get_resource_type
from tests.helpers import demo_rdb


def test_relation_handler_rdb_only():
    with demo_rdb() as rdb:
        relation_handler = ProvenanceHandler(rdb, False)
        intermediate = Intermediate(
            id=0,
            source=IntermediateSource.skema,
            type=IntermediateFormat.other,
            content=b"",
        )
        publication = Publication(id=0, xdd_uri="https://")

        # NOTE: Should these two asserts be their own test?
        assert get_resource_type(intermediate) == ResourceType.intermediate
        assert get_resource_type(publication) == ResourceType.publication

        id = relation_handler.create(
            intermediate, publication, RelationType.derivedfrom
        )
        assert relation_handler.retrieve(id) is not None
        assert relation_handler.delete(id)
        assert relation_handler.retrieve(id) is None
