"""
Tests basic model crud
"""

from tds.autogen.schema import IntermediateFormat, IntermediateSource, ValueType
from tds.schema.model import Intermediate, ModelFramework
from tests.helpers import demo_api


def test_framework_crd():
    """
    Test creation, retrieval and delete operations for framework.

    Note: There currently isn't a way to modify intermediates so an
          update has not been implemented
    """
    with demo_api("models") as client:
        # Creation
        payload = {"name": "dummy", "version": "v0", "semantics": ""}
        response_post = client.post(
            "/models/frameworks",
            json=payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        assert 200 == response_post.status_code
        id = response_post.json()
        # Retrieval
        response_get = client.get(
            f"/models/frameworks/{id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get.status_code
        result = ModelFramework.parse_obj(response_get.json())
        assert payload["name"] == result.name
        # Deletion
        response_delete = client.delete(f"/models/frameworks/{id}")
        assert 204 == response_delete.status_code
        response_get_fail = client.get(
            f"/models/frameworks/{id}", headers={"Accept": "application/json"}
        )
        assert response_get_fail.status_code == 404


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
        assert id != new_id
        assert 201 == response_update.status_code
        response_get_again = client.get(
            f"/models/{new_id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get_again.status_code
        assert response_get.json()["name"] != response_get_again.json()["name"]
        assert (
            "type" in new_payload["parameters"][0]
            and new_payload["parameters"][0]["type"] == ValueType.int
        )
