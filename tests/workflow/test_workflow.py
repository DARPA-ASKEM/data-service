"""
Model test for TDS.
"""
import os

import pytest
from sqlalchemy import create_engine

from tds.db.base import Base


class TestWorkflowEndpoints:
    def test_post(self, fast_api_fixture, fast_api_test_url, workflow_json):
        response = fast_api_fixture.post(
            url=f"{fast_api_test_url}/workflows",
            json=workflow_json,
        )
        response_json = response.json()
        assert response.status_code == 201
        assert "id" in response_json
        pytest.workflow_id = response_json["id"]

    def test_put(self, fast_api_fixture, fast_api_test_url, workflow_json):
        put_data = workflow_json
        new_name = "{name} updated".format(name=workflow_json["name"])
        put_data["id"] = pytest.workflow_id
        put_data["name"] = new_name
        response = fast_api_fixture.put(
            url=f"{fast_api_test_url}/workflows/{pytest.workflow_id}",
            json=put_data,
        )
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json and response_json["id"] == pytest.workflow_id

    def test_get(self, fast_api_fixture, fast_api_test_url, workflow_json):
        response = fast_api_fixture.get(
            url=f"{fast_api_test_url}/workflows/{pytest.workflow_id}",
        )
        response_json = response.json()
        new_name = "{name} updated".format(name=workflow_json["name"])
        assert response.status_code == 200
        assert "id" in response_json and response_json["id"] == pytest.workflow_id
        assert "timestamp" in response_json
        assert "name" in response_json and response_json["name"] == new_name

    def test_post_fail(self, fast_api_fixture, fast_api_test_url, workflow_json):
        fail_data = workflow_json
        del fail_data["name"]
        del fail_data["transform"]
        del fail_data["nodes"]
        response = fast_api_fixture.post(
            url=f"{fast_api_test_url}/workflows",
            json=workflow_json,
        )
        response_json = response.json()
        assert response.status_code == 422
        assert "detail" in response_json

    def test_put_fail(self, fast_api_fixture, fast_api_test_url, workflow_json):
        fail_data = workflow_json
        del fail_data["name"]
        del fail_data["transform"]
        del fail_data["nodes"]
        response = fast_api_fixture.put(
            url=f"{fast_api_test_url}/workflows/{pytest.workflow_id}",
            json=workflow_json,
        )
        response_json = response.json()
        assert response.status_code == 422
        assert "detail" in response_json

    def test_get_fail(self, fast_api_fixture, fast_api_test_url):
        response = fast_api_fixture.get(
            url=f"{fast_api_test_url}/workflows/id-does-not-exist",
        )
        assert response.status_code == 404
