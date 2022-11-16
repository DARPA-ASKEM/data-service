"""
Tests basic sim functionality
"""

from tds.autogen.schema import ValueType
from tests.helpers import demo_api


def test_simulation_cr():
    """
    Test creation, retrieval operations for results and plans.

    Note: Deletion is not implemented because we wouldn't want to mess up the Provenance graph.
    """
    with demo_api("simulations", "models") as client:
        # Preamble
        payload = {"name": "dummy", "version": "v0", "semantics": ""}
        framework = client.post(
            "/models/frameworks",
            json=payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        ).json()

        ## Create initial models
        model = {
            "name": "Foo",
            "description": "Lorem ipsum dolor sit amet.",
            "content": "{}",
            "parameters": {"x": ValueType.int},
            "framework": framework,
        }
        model_id = client.post(
            "/models",
            json=model,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        ).json()["id"]
        # Create
        payload = {
            "model_id": model_id,
            "simulator": "string",
            "query": "string",
            "content": "{}",
            "parameters": {"x": ("1", ValueType.int)},
            "framework": framework,
        }
        response_create = client.post(
            "/simulations/plans",
            json=payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        assert 200 == response_create.status_code
        id = response_create.json()
        # Retrieval
        response_get = client.get(
            f"/simulations/plans/{id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_create.status_code
        plan = response_get.json()
        assert payload["model_id"] == plan["model_id"]
        assert "x" in plan["parameters"] and plan["parameters"]["x"][1] == ValueType.int
        run_payload = {
            "simulator_id": id,
            "success": None,
            "completed_at": None,
            "response": "",
        }
        response_create = client.post(
            "/simulations/results",
            json=run_payload,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        assert 200 == response_create.status_code
        run_id = response_create.json()
        response_get = client.get(
            f"/simulations/results/{run_id}", headers={"Accept": "application/json"}
        )
        assert 200 == response_get.status_code
        assert run_payload["simulator_id"] == response_get.json()["simulator_id"]
