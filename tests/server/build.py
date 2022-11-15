"""
Test the API bundler
"""

from fastapi.testclient import TestClient

from tds.server.build import build_api


def test_build_api() -> None:
    """
    Ensure that the API can be built
    """
    client = TestClient(build_api())
    response = client.get("/")
    assert response.status_code == 200
