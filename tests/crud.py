"""
Specify an interface for testing CRUD
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from fastapi.testclient import TestClient

from tests.helpers import demo_api_context


class AllowedMethod(Enum):
    POST = 201
    GET = 200
    PUT = 200
    DELETE = 204


class CRUD(ABC):
    enabled_routers: List[str] = []

    def fetch(
        self,
        path: str,
        method: AllowedMethod = AllowedMethod.GET,
        payload: Optional[Dict] = None,
    ) -> Tuple[Any, int]:
        match method:
            case AllowedMethod.POST:
                response = self.client.post(
                    path,
                    json=payload,
                    headers={
                        "Content-type": "application/json",
                        "Accept": "text/plain",
                    },
                )
            case AllowedMethod.GET:
                response = self.client.get(path, headers={"Accept": "application/json"})
            case AllowedMethod.PUT:
                response = self.client.put(
                    path,
                    json=payload,
                    headers={
                        "Content-type": "application/json",
                        "Accept": "text/plain",
                    },
                )
            case AllowedMethod.DELETE:
                response = self.client.delete(
                    path, headers={"Accept": "application/json"}
                )

        if AllowedMethod.DELETE == method:
            return None, response.status_code

        return response.json(), response.status_code

    def teardown_method(self):
        self.ctx.__exit__(None, None, None)

    def setup_method(self):
        routers = self.__class__().enabled_routers
        self.ctx = demo_api_context(*routers)
        self.client, self.rdb = self.ctx.__enter__()
        self.init_test_data()

    @abstractmethod
    def init_test_data(self):
        pass

    @abstractmethod
    def test_rest_create(self):
        pass

    @abstractmethod
    def test_rest_retrieve(self):
        pass

    @abstractmethod
    def test_rest_update(self):
        pass

    @abstractmethod
    def test_rest_delete(self, router: TestClient):
        pass
