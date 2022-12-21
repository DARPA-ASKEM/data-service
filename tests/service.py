"""
Enforce client-expected features
"""

from pytest import mark
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.autogen.schema import IntermediateFormat, IntermediateSource, ValueType
from tds.schema.model import Intermediate, ModelFramework
from tds.schema.resource import Publication, Software
from tests.suite import AllowedMethod
from tests.suite import ASKEMEntityTestSuite as AETS
from tests.suite import expected_status


class TestFramework(AETS):
    enabled_routers = ["models"]

    def init_test_data(self):
        with Session(self.rdb) as session:
            framework = orm.ModelFramework(name="dummy", version="v0", semantics="")
            session.add(framework)
            session.commit()

    def test_rest_create(self):
        # Arrange
        payload = {"name": "create_dummy", "version": "v0", "semantics": ""}

        # Act
        create_response, create_status = self.fetch(
            "/models/frameworks", AllowedMethod.POST, payload
        )
        _, retrieve_status = self.fetch("/models/frameworks/create_dummy")

        # Assert
        assert create_status == expected_status[AllowedMethod.POST]
        assert create_response["name"] == "create_dummy"
        assert retrieve_status == expected_status[AllowedMethod.GET]

    def test_rest_retrieve(self):
        # Act
        response, status = self.fetch("/models/frameworks/dummy")
        framework = ModelFramework.parse_obj(response)

        # Assert
        assert status == expected_status[AllowedMethod.GET]
        assert framework.name == "dummy"
        assert framework.version == "v0"
        assert framework.semantics == ""

    @mark.skip(reason="update not implemented for frameworks")
    def test_rest_update(self):
        raise Exception("Framework object cannot be updated")

    def test_rest_delete(self):
        # Act
        _, delete_status = self.fetch("/models/frameworks/dummy", AllowedMethod.DELETE)
        _, retrieve_status = self.fetch("/models/frameworks/dummy")

        # Assert
        assert delete_status == expected_status[AllowedMethod.DELETE]
        assert retrieve_status == 404


# NOTE: Individual testing of model parameter and model description endpoints missing
class TestModel(AETS):
    enabled_routers = ["models"]

    def init_test_data(self):
        with Session(self.rdb) as session:
            framework = orm.ModelFramework(name="dummy", version="v0", semantics="")
            session.add(framework)
            session.commit()
            state = orm.ModelState(content="")
            session.add(state)
            session.commit()
            model = orm.ModelDescription(
                name="test_model",
                description="no text",
                framework=framework.name,
                state_id=state.id,
            )
            session.add(model)
            session.commit()
            param = orm.ModelParameter(
                model_id=model.id,
                name="first_test_param",
                default_value="1",
                type=ValueType.int,
                state_variable=False,
            )
            session.add(param)
            session.commit()

    def test_rest_create(self):
        # Arrange
        payload = {
            "name": "Foo",
            "description": "Lorem ipsum dolor sit amet.",
            "content": "{}",
            "parameters": [
                {
                    "name": "test_param",
                    "default_value": "1",
                    "type": ValueType.int,
                    "initial": False,
                }
            ],
            "framework": "dummy",
        }

        # Act
        create_response, create_status = self.fetch(
            "/models", AllowedMethod.POST, payload
        )
        _, retrieve_status = self.fetch("/models/2")

        # Assert
        assert create_status == expected_status[AllowedMethod.POST]
        assert create_response["id"] != 1
        assert retrieve_status == expected_status[AllowedMethod.GET]

    def test_rest_retrieve(self):
        # Act
        response, status = self.fetch("/models/1")

        # Assert
        assert status == expected_status[AllowedMethod.GET]
        assert response["name"] == "test_model"
        assert response["description"] == "no text"
        assert response["content"] == ""
        assert response["parameters"][0]["name"] == "first_test_param"
        assert response["framework"] == "dummy"

    def test_rest_update(self):
        # Arrange
        payload = {
            "name": "test_model",
            "description": "No desc",
            "framework": "dummy",
            "content": "[]",
            "parameters": [],
        }

        # Act
        _, update_status = self.fetch("/models/1", AllowedMethod.PUT, payload)
        retrieve_response, retrieve_status = self.fetch("/models/1")

        # Assert
        assert update_status == expected_status[AllowedMethod.PUT]
        assert retrieve_status == expected_status[AllowedMethod.GET]
        assert retrieve_response["name"] == "test_model"
        assert retrieve_response["description"] == "No desc"
        assert retrieve_response["content"] == []

    @mark.skip(reason="delete is an illegal action for models")
    def test_rest_delete(self):
        raise Exception("A model cannot be deleted")


class TestIntermediate(AETS):
    enabled_routers = ["models"]

    def init_test_data(self):
        with Session(self.rdb) as session:
            intermediate = orm.Intermediate(
                source=IntermediateSource.skema,
                type=IntermediateFormat.gromet,
                content=b"",
            )
            session.add(intermediate)
            session.commit()

    def test_rest_create(self):
        # Arrange
        payload = {
            "source": IntermediateSource.skema,
            "type": IntermediateFormat.gromet,
            "content": "",
        }

        # Act
        create_response, create_status = self.fetch(
            "/models/intermediates", AllowedMethod.POST, payload
        )
        _, retrieve_status = self.fetch("/models/intermediates/2")

        # Assert
        assert create_status == expected_status[AllowedMethod.POST]
        assert create_response["id"] != 1
        assert retrieve_status == expected_status[AllowedMethod.GET]

    def test_rest_retrieve(self):
        # Act
        response, status = self.fetch("/models/intermediates/1")
        intermediate = Intermediate.parse_obj(response)

        # Assert
        assert status == expected_status[AllowedMethod.GET]
        assert intermediate.source == IntermediateSource.skema
        assert intermediate.type == IntermediateFormat.gromet
        assert intermediate.content == b""

    @mark.skip(reason="update not implemented for intermediates")
    def test_rest_update(self):
        raise Exception("Intermediate object cannot be updated")

    def test_rest_delete(self):
        # Act
        _, delete_status = self.fetch("/models/intermediates/1", AllowedMethod.DELETE)
        _, retrieve_status = self.fetch("/models/intermediates/1")

        # Assert
        assert delete_status == expected_status[AllowedMethod.DELETE]
        assert retrieve_status == 404


class TestPublication(AETS):
    enabled_routers = ["external"]

    def init_test_data(self):
        with Session(self.rdb) as session:
            publication = orm.Publication(xdd_uri="fake", title="test")
            session.add(publication)
            session.commit()

    def test_rest_create(self):
        # Arrange
        payload = {
            "title": "created_test",
            "xdd_uri": "fake",
        }

        # Act
        create_response, create_status = self.fetch(
            "/external/publications", AllowedMethod.POST, payload
        )
        _, retrieve_status = self.fetch("/external/publications/2")

        # Assert
        assert create_status == expected_status[AllowedMethod.POST]
        assert create_response["id"] != 1
        assert retrieve_status == expected_status[AllowedMethod.GET]

    def test_rest_retrieve(self):
        # Act
        response, status = self.fetch("/external/publications/1")
        software = Publication.parse_obj(response)

        # Assert
        assert status == expected_status[AllowedMethod.GET]
        assert software.title == "test"
        assert software.xdd_uri == "fake"

    @mark.skip(reason="update not implemented for publications")
    def test_rest_update(self):
        raise Exception("Publication object cannot be updated")

    def test_rest_delete(self):
        # Act
        _, delete_status = self.fetch("/external/publications/1", AllowedMethod.DELETE)
        _, retrieve_status = self.fetch("/external/publications/1")

        # Assert
        assert delete_status == expected_status[AllowedMethod.DELETE]
        assert retrieve_status == 404


class TestSoftware(AETS):
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
        assert create_status == expected_status[AllowedMethod.POST]
        assert create_response["id"] != 1
        assert retrieve_status == expected_status[AllowedMethod.GET]

    def test_rest_retrieve(self):
        # Act
        response, status = self.fetch("/external/software/1")
        software = Software.parse_obj(response)

        # Assert
        assert status == expected_status[AllowedMethod.GET]
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
        assert delete_status == expected_status[AllowedMethod.DELETE]
        assert retrieve_status == 404
