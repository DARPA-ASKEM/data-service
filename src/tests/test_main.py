from fastapi.testclient import TestClient

from src.main import build_api, DBML_PATH, DBML_VERSION
from src.generation.gen import get_dbml_version


def test_version() -> None:
    assert DBML_VERSION == get_dbml_version(DBML_PATH)


def test_build_api() -> None:
    client = TestClient(build_api())
    response = client.get("/")
    assert response.status_code == 200
