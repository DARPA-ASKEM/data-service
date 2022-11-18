"""
Tests basic model crud
"""

from tds.autogen.schema import ResourceType, ValueType
from tests.helpers import demo_api


def test_project_cru():
    """
    Test creation, retrieval and delete operations for modify.

    Note: Deletion is not implemented because we wouldn't want to mess up the Provenance graph.
    """
    with demo_api("projects", "models") as client:
        # Preamble
        payload = {"name": "dummy", "version": "v0", "semantics": ""}
        framework = client.post(
            "/models/frameworks",
            json=payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        ).json()

        ## Create initial models
        model1 = {
            "name": "Foo",
            "description": "Lorem ipsum dolor sit amet.",
            "content": "{}",
            "parameters": {"x": ValueType.int},
            "framework": framework,
        }
        model2 = {
            "name": "Foo2",
            "description": "Lorem ipsum dolor sit amet.",
            "content": "[]",
            "parameters": {"y": ValueType.int},
            "framework": framework,
        }
        model1_id = client.post(
            "/models",
            json=model1,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        ).json()["id"]
        model2_id = client.post(
            "/models",
            json=model2,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        ).json()["id"]

        # Create
        payload = {
            "name": "string",
            "description": "string",
            "assets": {ResourceType.models: [model1_id]},
        }
        response_create = client.post(
            "/projects",
            json=payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        assert 201 == response_create.status_code
        id = response_create.json()["id"]
        # Retrieval
        response_get = client.get(
            f"/projects/{id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get.status_code
        project = response_get.json()
        assert payload["name"] == project["name"]
        assert (
            ResourceType.models in project["assets"]
            and model1_id in project["assets"][ResourceType.models]
        )
        # Update
        payload_updated = {
            "name": "new_string",
            "description": "string",
            "assets": {ResourceType.models: [model2_id]},
        }
        response_update = client.put(
            f"/projects/{id}",
            json=payload_updated,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        assert 200 == response_update.status_code
        response_get_again = client.get(
            f"/projects/{id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get_again.status_code
        project = response_get_again.json()
        assert response_get.json()["name"] != response_get_again.json()["name"]
        assert (
            ResourceType.models in project["assets"]
            and model2_id in project["assets"][ResourceType.models]
            and model1_id not in project["assets"][ResourceType.models]
        )
