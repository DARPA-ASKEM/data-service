"""
tests.main - A basic healthcheck
"""

from dbml_builder import get_dbml_version
from fastapi.testclient import TestClient

from src.main import build_api
from src.settings import settings
from tests.utils import demo_engine


def test_version() -> None:
    """
    Ensure the code is not using an outdated version of the DBML
    """
    assert settings.dbml_version == get_dbml_version(settings.dbml_path)


def test_build_api() -> None:
    """
    Ensure that the API can be built
    """
    with demo_engine() as engine:
        client = TestClient(build_api(engine))
        response = client.get("/")
        assert response.status_code == 200
