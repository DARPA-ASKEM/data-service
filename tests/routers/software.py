"""
tests.routers.software - NOT FULLY IMPLEMENTED
"""

from sqlalchemy.exc import InvalidRequestError

from src.autogen.schema import Software
from tests.utils import demo_api


def test_software_crd():
    """
    Test creation, retrieval and delete operations for software.

    Note: There currently isn't a way to modify sofware so an
          update has not been implemented
    """
    with demo_api("software") as client:
        # Creation
        software = Software(source="test", storage_uri="http://")
        response_post = client.post(
            "/software",
            data=software.json(),
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        assert 200 == response_post.status_code
        id = response_post.json()
        # Retrieval
        response_get = client.get(
            f"/software/{id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get.status_code
        result = Software.parse_obj(response_get.json())
        assert (
            software.source == result.source
            and software.storage_uri == result.storage_uri
        )
        # Deletion
        client.delete(f"/software/{id}")
        try:
            response_get = client.get(
                f"/software/{id}", headers={"Accept": "application/json"}
            )
        except Exception as e:
            print(e)
        else:
            raise AssertionError("Item failed to delete")
