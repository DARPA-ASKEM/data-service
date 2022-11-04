"""
tests.relation.provenance - Test provenance wrapper
"""
from tds.autogen.schema import (
    Intermediate,
    IntermediateFormat,
    IntermediateSource,
    Publication,
    RelationType,
)
from tds.relation.provenance import RelationHandler
from tests.helpers import demo_rdb


def test_relation_handler_rdb_only():
    relation_handler = RelationHandler(demo_rdb(), False)
    intermediate = Intermediate(
        source=IntermediateSource.skema,
        type=IntermediateFormat.other,
        representation=b"",
    )
    publication = Publication(xdd_uri="https://")
    id = relation_handler.create(intermediate, publication, RelationType.derivedfrom)
    assert relation_handler.retrieve(id) is not None
    assert relation_handler.delete(id)
    assert relation_handler.retrieve(id) is None
