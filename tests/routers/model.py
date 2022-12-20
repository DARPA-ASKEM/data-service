"""
Enforce model object
"""

from tds.autogen.schema import ValueType
from tests.helpers import demo_api


def test_model_cru():
    """
    Test creation, retrieval and delete operations for modify.

    Note: Deletion is not implemented because we wouldn't want to mess up the Provenance graph.
    """
    with demo_api("models") as client:
        # Preamble
        payload = {"name": "dummy", "version": "v0", "semantics": ""}
        framework = client.post(
            "/models/frameworks",
            json=payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        ).json()

        # Creation
        payload = {
            "name": "Foo",
            "description": "Lorem ipsum dolor sit amet.",
            "content": "{}",
            "parameters": [
                {
                    "name": "test",
                    "default_value": "1",
                    "type": ValueType.int,
                    "initial": False,
                }
            ],
            "framework": framework,
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
            "type" in payload["parameters"][0]
            and payload["parameters"][0]["type"] == ValueType.int
        )
        # Update
        new_payload = {
            "name": "Bar",
            "description": "No desc",
            "content": "[]",
            "parameters": [
                {
                    "name": "test",
                    "default_value": "2",
                    "type": ValueType.int,
                    "initial": False,
                }
            ],
            "framework": framework,
        }
        response_update = client.post(
            f"/models/{id}",
            json=new_payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        new_id = response_update.json()["id"]
        assert 200 == response_update.status_code
        response_get_again = client.get(
            f"/models/{new_id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get_again.status_code
        assert response_get.json()["name"] != response_get_again.json()["name"]
        assert (
            "type" in new_payload["parameters"][0]
            and new_payload["parameters"][0]["type"] == ValueType.int
        )
