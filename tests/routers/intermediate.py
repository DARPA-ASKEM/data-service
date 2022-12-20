"""
Enforce intermediate interface
"""

from tds.autogen.schema import IntermediateFormat, IntermediateSource
from tds.schema.model import Intermediate
from tests.helpers import demo_api


def test_intermediate_crd():
    """
    Test creation, retrieval and delete operations for intermediates.

    Note: There currently isn't a way to modify intermediates so an
          update has not been implemented
    """
    with demo_api("models") as client:
        # Creation
        payload = {
            "source": IntermediateSource.skema,
            "type": IntermediateFormat.gromet,
            "content": "",
        }
        response_post = client.post(
            "/models/intermediates",
            json=payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        assert 201 == response_post.status_code
        id = response_post.json()["id"]
        # Retrieval
        response_get = client.get(
            f"/models/intermediates/{id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get.status_code
        result = Intermediate.parse_obj(response_get.json())
        assert payload["source"] == result.source and payload["type"] == result.type
        # Deletion
        response_delete = client.delete(f"/models/intermediates/{id}")
        assert 204 == response_delete.status_code
        response_get_fail = client.get(
            f"/models/intermediates/{id}", headers={"Accept": "application/json"}
        )
        assert response_get_fail.status_code == 404
