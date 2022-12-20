"""
Enforce framework interface
"""

from tds.schema.model import ModelFramework
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
