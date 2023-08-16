"""
Code module test for TDS.
"""
import pytest


class TestCodeEndpoints:
    def test_post(self, fast_api_fixture, fast_api_test_url, code_json):
        response = fast_api_fixture.post(
            url=f"{fast_api_test_url}/code",
            json=code_json,
        )
        response_json = response.json()
        assert response.status_code == 201
        assert "id" in response_json
        pytest.code_id = response_json["id"]

    def test_put(self, fast_api_fixture, fast_api_test_url, code_json):
        put_data = code_json
        new_name = "{name} updated".format(name=code_json["name"])
        put_data["id"] = pytest.code_id
        put_data["name"] = new_name
        response = fast_api_fixture.put(
            url=f"{fast_api_test_url}/code/{pytest.code_id}",
            json=put_data,
        )
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json and response_json["id"] == pytest.code_id

    def test_get(self, fast_api_fixture, fast_api_test_url, code_json):
        response = fast_api_fixture.get(
            url=f"{fast_api_test_url}/code/{pytest.code_id}",
        )
        response_json = response.json()
        new_name = "{name} updated".format(name=code_json["name"])
        assert response.status_code == 200
        assert "id" in response_json and response_json["id"] == pytest.code_id
        assert "timestamp" in response_json
        assert "name" in response_json and response_json["name"] == new_name

    def test_post_fail(self, fast_api_fixture, fast_api_test_url, code_json):
        fail_data = code_json
        del fail_data["name"]
        del fail_data["filename"]
        response = fast_api_fixture.post(
            url=f"{fast_api_test_url}/code",
            json=code_json,
        )
        response_json = response.json()
        assert response.status_code == 422
        assert "detail" in response_json

    def test_put_fail(self, fast_api_fixture, fast_api_test_url, code_json):
        fail_data = code_json
        del fail_data["name"]
        del fail_data["filename"]
        response = fast_api_fixture.put(
            url=f"{fast_api_test_url}/code/{pytest.code_id}",
            json=code_json,
        )
        response_json = response.json()
        assert response.status_code == 422
        assert "detail" in response_json

    def test_get_fail(self, fast_api_fixture, fast_api_test_url):
        response = fast_api_fixture.get(
            url=f"{fast_api_test_url}/code/id-does-not-exist",
        )
        assert response.status_code == 404
