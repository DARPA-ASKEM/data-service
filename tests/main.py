"""
tests.main - A basic healthcheck
"""

from dbml_builder import get_dbml_version
from fastapi.testclient import TestClient

from tds.server.build import build_api
from tds.settings import settings


def test_version() -> None:
    """
    Ensure the code is not using an outdated version of the DBML
    """
    assert settings.DBML_VERSION == get_dbml_version(settings.DBML_PATH)


def test_build_api() -> None:
    """
    Ensure that the API can be built
    """
    client = TestClient(build_api())
    response = client.get("/")
    assert response.status_code == 200
