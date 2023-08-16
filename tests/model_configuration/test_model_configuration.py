"""
Model test for TDS.
"""
import os

import pytest
from sqlalchemy import create_engine

from tds.db.base import Base


class TestModelConfigurationEndpoints:
    def test_post(self, fast_api_fixture, fast_api_test_url, model_config_json):
        response = fast_api_fixture.post(
            url=f"{fast_api_test_url}/model_configurations",
            json=model_config_json,
        )
        response_json = response.json()
        assert response.status_code == 201
        assert "id" in response_json
        pytest.model_configuration_id = response_json["id"]

    def test_put(self, fast_api_fixture, fast_api_test_url, model_config_json):
        put_data = model_config_json
        new_name = "{name} updated".format(name=model_config_json["name"])
        put_data["id"] = pytest.model_configuration_id
        put_data["name"] = new_name
        response = fast_api_fixture.put(
            url=f"{fast_api_test_url}/model_configurations/{pytest.model_configuration_id}",
            json=put_data,
        )
        response_json = response.json()
        assert response.status_code == 200
        assert (
            "id" in response_json
            and response_json["id"] == pytest.model_configuration_id
        )

    def test_get(self, fast_api_fixture, fast_api_test_url):
        response = fast_api_fixture.get(
            url=f"{fast_api_test_url}/model_configurations/{pytest.model_configuration_id}",
        )
        response_json = response.json()
        assert response.status_code == 200
        assert (
            "id" in response_json
            and response_json["id"] == pytest.model_configuration_id
        )
        assert "timestamp" in response_json

    def test_post_fail(self, fast_api_fixture, fast_api_test_url, model_config_json):
        fail_data = model_config_json
        del fail_data["name"]
        del fail_data["configuration"]
        response = fast_api_fixture.post(
            url=f"{fast_api_test_url}/model_configurations",
            json=model_config_json,
        )
        response_json = response.json()
        assert response.status_code == 422
        assert "detail" in response_json

    def test_put_fail(self, fast_api_fixture, fast_api_test_url, model_config_json):
        fail_data = model_config_json
        del fail_data["name"]
        del fail_data["configuration"]
        response = fast_api_fixture.put(
            url=f"{fast_api_test_url}/model_configurations/{pytest.model_configuration_id}",
            json=model_config_json,
        )
        response_json = response.json()
        assert response.status_code == 422
        assert "detail" in response_json

    def test_get_fail(self, fast_api_fixture, fast_api_test_url):
        response = fast_api_fixture.get(
            url=f"{fast_api_test_url}/model_configurations/id-does-not-exist",
        )
        assert response.status_code == 404
