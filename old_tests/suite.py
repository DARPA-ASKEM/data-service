"""
Specify an interface for testing CRUD
"""

# pylint: disable=no-member, unnecessary-dunder-call, attribute-defined-outside-init

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from tests.helpers import demo_api_context


class AllowedMethod(Enum):
    """
    The methods we will test over
    """

    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"


expected_status = {
    AllowedMethod.POST: 201,
    AllowedMethod.GET: 200,
    AllowedMethod.PUT: 200,
    AllowedMethod.DELETE: 204,
}


class ASKEMEntityTestSuite(ABC):
    """
    A Test Suite that provides common functions.

    The service provides ASKEM entities which should behave in a relatively
    uniform way.
    """

    enabled_routers: List[str] = []

    def fetch(
        self,
        path: str,
        method: AllowedMethod = AllowedMethod.GET,
        payload: Optional[Dict] = None,
    ) -> Tuple[Any, int]:
        """
        Standardize HTTP calls and provide relevant data for testing
        """
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
                return None, response.status_code

        if response.status_code > 300:
            return None, response.status_code

        return response.json(), response.status_code

    def teardown_method(self):
        """
        Exit `with` context of the `demo_api`
        """
        if getattr(self, "ctx", None) is None:
            return
        self.ctx.__exit__(None, None, None)
        self.ctx = None

    def setup_method(self):
        """
        Enter `with` context of the `demo_api`
        """
        routers = self.__class__().enabled_routers
        self.ctx = demo_api_context(*routers)
        self.client, self.rdb = self.ctx.__enter__()
        self.init_test_data()

    @abstractmethod
    def init_test_data(self):
        """
        Initialize the test data directly using SQLAlchemy

        This will be called at the end of `setup_method`
        """
