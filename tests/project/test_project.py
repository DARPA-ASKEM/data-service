"""
Model test for TDS.
"""
import os

import pytest
from sqlalchemy import create_engine

from tds.db.base import Base


class TestProjectEndpoints:
    def test_post(self, fast_api_fixture, fast_api_test_url, project_json):
        response = fast_api_fixture.post(
            url=f"{fast_api_test_url}/projects",
            json=project_json,
        )
        response_json = response.json()
        assert response.status_code == 201
        assert "id" in response_json
        pytest.project_id = response_json["id"]

    def test_put(self, fast_api_fixture, fast_api_test_url, project_json):
        put_data = project_json
        new_name = "{name} updated".format(name=project_json["name"])
        put_data["id"] = pytest.project_id
        put_data["name"] = new_name
        response = fast_api_fixture.put(
            url=f"{fast_api_test_url}/projects/{pytest.project_id}",
            json=put_data,
        )
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json and response_json["id"] == pytest.project_id

    def test_get(self, fast_api_fixture, fast_api_test_url):
        response = fast_api_fixture.get(
            url=f"{fast_api_test_url}/projects/{pytest.project_id}",
        )
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json and response_json["id"] == pytest.project_id
        assert "timestamp" in response_json

    def test_post_fail(self, fast_api_fixture, fast_api_test_url, project_json):
        fail_data = project_json
        del fail_data["name"]
        del fail_data["active"]
        response = fast_api_fixture.post(
            url=f"{fast_api_test_url}/projects",
            json=project_json,
        )
        response_json = response.json()
        assert response.status_code == 422
        assert "detail" in response_json

    def test_put_fail(self, fast_api_fixture, fast_api_test_url, project_json):
        fail_data = project_json
        del fail_data["name"]
        del fail_data["active"]
        response = fast_api_fixture.put(
            url=f"{fast_api_test_url}/projects/{pytest.project_id}",
            json=project_json,
        )
        response_json = response.json()
        assert response.status_code == 422
        assert "detail" in response_json

    def test_get_fail(self, fast_api_fixture, fast_api_test_url):
        response = fast_api_fixture.get(
            url=f"{fast_api_test_url}/projects/18202",
        )
        assert response.status_code == 404
