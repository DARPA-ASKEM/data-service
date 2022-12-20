"""
Enforce client-expected features
"""

from pytest import mark
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.schema.resource import Software
from tests.crud import CRUD, AllowedMethod


class TestSoftware(CRUD):
    enabled_routers = ["external"]

    def init_test_data(self):
        with Session(self.rdb) as session:
            software = orm.Software(source="test", storage_uri="http://")
            session.add(software)
            session.commit()

    def test_rest_create(self):
        # Arrange
        payload = {"source": "creation_test", "storage_uri": "http://"}

        # Act
        create_response, create_status = self.fetch(
            "/external/software", AllowedMethod.POST, payload
        )
        _, retrieve_status = self.fetch("/external/software/2")

        # Assert
        assert create_status == AllowedMethod.POST.value
        assert create_response["id"] != 1
        assert retrieve_status == AllowedMethod.GET.value

    def test_rest_retrieve(self):
        # Act
        response, status = self.fetch("/external/software/1")
        software = Software.parse_obj(response)

        # Assert
        assert status == AllowedMethod.GET.value
        assert software.source == "test"
        assert software.storage_uri == "http://"

    @mark.skip(reason="update not implemented for software")
    def test_rest_update(self):
        raise Exception("Software object cannot be updated")

    def test_rest_delete(self):
        # Act
        _, delete_status = self.fetch("/external/software/1", AllowedMethod.DELETE)
        _, retrieve_status = self.fetch("/external/software/1")

        # Assert
        assert delete_status == AllowedMethod.DELETE.value
        assert retrieve_status == 404
