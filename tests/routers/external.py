"""
Tests basic external resources
"""

from tds.schema.resource import Publication, Software
from tests.helpers import demo_api


def test_software_crd():
    """
    Test creation, retrieval and delete operations for software.

    Note: There currently isn't a way to modify sofware so an
          update has not been implemented
    """
    with demo_api("external") as client:
        # Creation
        software = Software(source="test", storage_uri="http://")
        response_post = client.post(
            "/external/software",
            data=software.json(),
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        assert 201 == response_post.status_code
        id = response_post.json()["id"]
        # Retrieval
        response_get = client.get(
            f"/external/software/{id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get.status_code
        result = Software.parse_obj(response_get.json())
        assert (
            software.source == result.source
            and software.storage_uri == result.storage_uri
        )
        # Deletion
        response_delete = client.delete(f"/external/software/{id}")
        assert 204 == response_delete.status_code
        response_get_fail = client.get(
            f"/external/software/{id}", headers={"Accept": "application/json"}
        )
        assert response_get_fail.status_code == 404


def test_publication_crd():
    """
    Test creation, retrieval and delete operations for publication.

    Note: There currently isn't a way to modify publications so an
          update has not been implemented
    """
    with demo_api("external") as client:
        # Creation
        publication = Publication(xdd_uri="fake")
        response_post = client.post(
            "/external/publications",
            data=publication.json(),
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        assert 201 == response_post.status_code
        id = response_post.json()["id"]
        # Retrieval
        response_get = client.get(
            f"/external/publications/{id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get.status_code
        result = Publication.parse_obj(response_get.json())
        assert publication.xdd_uri == result.xdd_uri
        # Deletion
        response_delete = client.delete(f"/external/publications/{id}")
        assert 204 == response_delete.status_code
        response_get_fail = client.get(
            f"/external/publications/{id}", headers={"Accept": "application/json"}
        )
        assert response_get_fail.status_code == 404
