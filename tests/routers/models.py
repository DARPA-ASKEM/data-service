"""
Tests basic model crud
"""

from tds.autogen.schema import ValueType
from tests.helpers import demo_api


def test_model_cru():
    """
    Test creation, retrieval and delete operations for modify.

    Note: Deletion is not implemented because we wouldn't want to mess up the Provenance graph.
    """
    with demo_api("models") as client:
        # Creation
        payload = {
            "name": "Foo",
            "description": "Lorem ipsum dolor sit amet.",
            "content": "{}",
            "parameters": {"x": ValueType.int},
        }
        response_create = client.post(
            "/models",
            json=payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        assert 201 == response_create.status_code
        id = response_create.json()["id"]
        # Retrieval
        response_get = client.get(
            f"/models/{id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get.status_code
        assert payload["name"] == response_get.json()["name"]
        assert (
            "x" in payload["parameters"] and payload["parameters"]["x"] == ValueType.int
        )
        # Update
        new_payload = {
            "name": "Bar",
            "description": "No desc",
            "content": "[]",
            "parameters": {"y": ValueType.bool},
        }
        response_update = client.post(
            f"/models/{id}",
            json=new_payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        new_id = response_update.json()["id"]
        assert id != new_id
        assert 201 == response_update.status_code
        response_get_again = client.get(
            f"/models/{new_id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get_again.status_code
        assert response_get.json()["name"] != response_get_again.json()["name"]
        assert (
            "y" in new_payload["parameters"]
            and new_payload["parameters"]["y"] == ValueType.bool
        )
