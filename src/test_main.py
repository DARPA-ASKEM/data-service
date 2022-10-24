"""
test.test_main - A basic healthcheck
"""

from fastapi.testclient import TestClient
from dbml_builder import get_dbml_version
from src.main import build_api, DBML_VERSION

DBML_PATH="../askem.dbml"

def test_version() -> None:
    """
    Ensure the code is not using an outdated version of the DBML
    """
    assert DBML_VERSION == get_dbml_version(DBML_PATH)


def test_build_api() -> None:
    """
    Ensure that the API can be built
    """
    client = TestClient(build_api())
    response = client.get("/")
    assert response.status_code == 200
