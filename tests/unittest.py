"""
Validate unit tests
"""

# from fastapi import Depends
from fastapi.testclient import TestClient

from tds.server.build import build_api
from tds.settings import settings

settings.ES_URL = "http://localhost:9200"


def test_build_api() -> None:
    """
    Ensure that the API can be built
    """
    client = TestClient(build_api())
    response = client.get("/")
    assert response.status_code == 200


def test_healthcheck() -> None:
    """
    Ensure healthcheck responds properly
    """

    client = TestClient(build_api())

    healthcheck_response = client.get("/health")

    assert healthcheck_response.status_code == 200
    assert healthcheck_response.json().get("status", None) == "ok"


def test_route_collection() -> None:
    from starlette.routing import Route

    api = build_api()

    # Five routes will be always exist: /openapi.json, /, /docs/oauth2-redirect, /redoc, /health
    # Note: /health is defined by us while the others are defined by FastAPI
    assert len(api.routes) > 5, "Should be at more than five routes"

    # Assert all routes are of Route class
    assert all(
        map(lambda route: isinstance(route, Route), api.routes)
    ), "Routes should be correctly defined"

    # Find the `/models` route and confirm the correct method(s) are set
    for route in api.routes:
        if route.path == "/models":
            model_route = route
            break
    else:
        assert False, "Model route is not defined"
    assert set(model_route.methods) == set(
        ["POST"]
    ), "/models route should only accept POST method"
