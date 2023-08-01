"""
Model test for TDS.
"""


class TestModelEndpoints:
    _model_id = None

    def test_post(
        self, _mock_elasticsearch, fast_api_fixture, fast_api_test_url, model_json
    ):
        response = fast_api_fixture.post(
            url=f"{fast_api_test_url}/models",
            json=model_json,
        )
        response_json = response.json()
        assert response.status_code == 201
        assert "id" in response_json
        self._model_id = response_json["id"]

    def test_put(
        self, _mock_elasticsearch, fast_api_fixture, fast_api_test_url, model_json
    ):
        put_data = model_json
        new_name = "{name} updated".format(name=model_json["name"])
        put_data["id"] = self._model_id
        put_data["name"] = new_name
        response = fast_api_fixture.put(
            url=f"{fast_api_test_url}/models/{self._model_id}",
            json=put_data,
        )
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json and response_json["id"] == self._model_id

    def test_get(
        self, _mock_elasticsearch, fast_api_fixture, fast_api_test_url, model_json
    ):
        response = fast_api_fixture.get(
            url=f"{fast_api_test_url}/models/{self._model_id}",
        )
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json and response_json["id"] == self._model_id
        assert "timestamp" in response_json

    def test_post_fail(
        self, _mock_elasticsearch, fast_api_fixture, fast_api_test_url, model_json
    ):
        fail_data = model_json
        del fail_data["name"]
        del fail_data["model"]
        response = fast_api_fixture.post(
            url=f"{fast_api_test_url}/models",
            json=model_json,
        )
        response_json = response.json()
        assert response.status_code == 422
        assert "detail" in response_json

    def test_put_fail(
        self, _mock_elasticsearch, fast_api_fixture, fast_api_test_url, model_json
    ):
        fail_data = model_json
        del fail_data["name"]
        del fail_data["model"]
        response = fast_api_fixture.put(
            url=f"{fast_api_test_url}/models/{self._model_id}",
            json=model_json,
        )
        response_json = response.json()
        assert response.status_code == 422
        assert "detail" in response_json

    def test_get_fail(
        self, _mock_elasticsearch, fast_api_fixture, fast_api_test_url, model_json
    ):
        response = fast_api_fixture.get(
            url=f"{fast_api_test_url}/models/id-does-not-exist",
        )
        assert response.status_code == 404
