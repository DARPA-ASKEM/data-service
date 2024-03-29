"""
Enforce client-expected features
"""
# pylint: disable=missing-class-docstring, missing-function-docstring

from pytest import mark
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db.enums import ResourceType, ValueType
from tds.modules.model.model import ModelFramework
from tds.schema.resource import Publication, Software
from tests.suite import AllowedMethod
from tests.suite import ASKEMEntityTestSuite as AETS
from tests.suite import expected_status


# TODO: The assets endpoints need testing
class TestProject(AETS):
    enabled_routers = ["projects"]

    def init_test_data(self):
        with Session(self.rdb) as session:
            # Arrange Models
            framework = ModelFramework(name="dummy", version="v0", semantics="")
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
            model2 = orm.ModelDescription(
                name="test_model_2",
                description="no text_again",
                framework=framework.name,
                state_id=state.id,
            )
            session.add(model2)
            session.commit()

            project = orm.Project(name="sample", description="no desc", active=True)
            session.add(project)
            session.commit()

            asset = orm.ProjectAsset(
                project_id=1,
                resource_id=1,
                resource_type=ResourceType.models,
                external_ref="https://",
            )
            session.add(asset)
            session.commit()

    def test_rest_create(self):
        # Arrange
        payload = {
            "name": "string",
            "description": "string",
            "assets": {ResourceType.models: [2]},
            "active": True,
        }
        # Act
        create_response, create_status = self.fetch(
            "/projects", AllowedMethod.POST, payload
        )
        _, retrieve_status = self.fetch("/projects/2")

        # Assert
        assert create_status == expected_status[AllowedMethod.POST]
        assert create_response["id"] != 1
        assert retrieve_status == expected_status[AllowedMethod.GET]

    def test_rest_retrieve(self):
        # Act
        response, status = self.fetch("/projects/1")

        # Assert
        assert status == expected_status[AllowedMethod.GET]
        assert response["name"] == "sample"
        assert response["description"] == "no desc"
        assert response["active"]
        assert len(response["assets"]["models"]) == 1

    def test_rest_update(self):
        # Arrange
        payload = {
            "name": "sample",
            "description": "new_desc",
            "assets": {ResourceType.models: [2]},
            "active": True,
        }
        # Act
        _, update_status = self.fetch("/projects/1", AllowedMethod.PUT, payload)
        retrieve_response, retrieve_status = self.fetch("/projects/1")

        # Assert
        assert update_status == expected_status[AllowedMethod.PUT]
        assert retrieve_status == expected_status[AllowedMethod.GET]
        assert retrieve_response["name"] == "sample"
        assert retrieve_response["description"] == "new_desc"
        assert retrieve_response["active"]
        assert len(retrieve_response["assets"]["models"]) == 1
        assert retrieve_response["assets"]["models"][0] == 2

    def test_rest_delete(self):
        # Act
        _, delete_status = self.fetch("/projects/1", AllowedMethod.DELETE)
        retrieve_response, retrieve_status = self.fetch("/projects/1")

        # Assert
        assert delete_status == 200
        assert retrieve_status == 200
        assert not retrieve_response["active"]


class TestRun(AETS):
    enabled_routers = ["simulations"]

    def init_test_data(self):
        with Session(self.rdb) as session:
            # Arrange Model
            framework = ModelFramework(name="dummy", version="v0", semantics="")
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
            model_param = orm.ModelParameter(
                model_id=model.id,
                name="first_test_param",
                default_value="1",
                type=ValueType.int,
                state_variable=False,
            )
            session.add(model_param)
            session.commit()

            # Arrange Sim
            config = orm.ModelConfiguration(
                name="default", model_id=model.id, content=""
            )
            session.add(config)
            session.commit()

            run = orm.SimulationRun(
                simulator_id=config.id,
                success=None,
                completed_at=None,
                response=b"sample",
            )
            session.add(run)
            session.commit()

            run_param = orm.SimulationParameter(
                run_id=run.id,
                name="x",
                value="1",
                type=ValueType.int,
            )
            session.add(run_param)
            session.commit()

    @mark.skip(reason="TODO: Add update functionality to simulation run")
    def test_rest_update(self):
        raise Exception("Run updates needs to be implemented")

    def test_rest_create(self):
        # Arrange
        payload = {
            "simulator_id": 1,
            "success": None,
            "completed_at": None,
            "parameters": [{"name": "y", "value": "2", "type": ValueType.int}],
            "response": "",
        }
        # Act
        create_response, create_status = self.fetch(
            "/simulations/runs", AllowedMethod.POST, payload
        )
        _, retrieve_status = self.fetch("/simulations/runs/2")

        # Assert
        assert create_status == expected_status[AllowedMethod.POST]
        assert create_response["id"] != 1
        assert retrieve_status == expected_status[AllowedMethod.GET]

    def test_rest_retrieve(self):
        # Act
        response, status = self.fetch("/simulations/runs/1")

        # Assert
        assert status == expected_status[AllowedMethod.GET]
        assert response["response"] == "sample"
        assert response["parameters"][0]["name"] == "x"


class TestModelConfig(AETS):
    enabled_routers = ["models", "simulations"]

    def init_test_data(self):
        with Session(self.rdb) as session:
            # Arrange Model
            framework = ModelFramework(name="dummy", version="v0", semantics="")
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

            # Arrange Sim
            config = orm.ModelConfiguration(
                name="default", model_id=model.id, content=""
            )
            session.add(config)
            session.commit()

    @mark.skip(reason="TODO: Add update functionality to model configuration")
    def test_rest_update(self):
        raise Exception("Configuration updates needs to be implemented")

    def test_rest_create(self):
        # Arrange
        payload = {
            "name": "Untitled(1)",
            "model_id": 1,
            "content": "{}",
        }

        # Act
        create_response, create_status = self.fetch(
            "/simulations/plans", AllowedMethod.POST, payload
        )
        _, retrieve_status = self.fetch("/simulations/plans/2")

        # Assert
        assert create_status == expected_status[AllowedMethod.POST]
        assert create_response["id"] != 1
        assert retrieve_status == expected_status[AllowedMethod.GET]

    def test_rest_retrieve(self):
        # Act
        response, status = self.fetch("/simulations/plans/1")

        # Assert
        assert status == expected_status[AllowedMethod.GET]
        assert response["content"] == ""


# TODO: Individual testing of model parameter and model description endpoints missing
class TestModel(AETS):
    enabled_routers = ["models"]

    def init_test_data(self):
        with Session(self.rdb) as session:
            framework = ModelFramework(name="dummy", version="v0", semantics="")
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
        _, update_status = self.fetch("/models/1", AllowedMethod.POST, payload)
        retrieve_response, retrieve_status = self.fetch("/models/1")

        # Assert
        assert update_status == expected_status[AllowedMethod.PUT]
        assert retrieve_status == expected_status[AllowedMethod.GET]
        assert retrieve_response["name"] == "test_model"
        assert retrieve_response["description"] == "No desc"
        assert retrieve_response["content"] == []


class TestFramework(AETS):
    enabled_routers = ["models"]

    def init_test_data(self):
        with Session(self.rdb) as session:
            framework = ModelFramework(name="dummy", version="v0", semantics="")
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

    def test_rest_delete(self):
        # Act
        _, delete_status = self.fetch("/models/frameworks/dummy", AllowedMethod.DELETE)
        _, retrieve_status = self.fetch("/models/frameworks/dummy")

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
        payload_new = {
            "title": "created_test",
            "xdd_uri": "fake2",
        }

        payload_not_new = {
            "title": "not_new_test",
            "xdd_uri": "fake",
        }

        # Act
        create_response_new, create_status_new = self.fetch(
            "/external/publications", AllowedMethod.POST, payload_new
        )
        _, create_status_not_new = self.fetch(
            "/external/publications", AllowedMethod.POST, payload_not_new
        )
        _, retrieve_status = self.fetch("/external/publications/2")

        # Assert
        assert create_status_new == expected_status[AllowedMethod.POST]
        assert create_response_new["id"] != 1
        assert create_status_not_new == 200
        assert retrieve_status == expected_status[AllowedMethod.GET]

    def test_rest_retrieve(self):
        # Act
        response, status = self.fetch("/external/publications/1")
        software = Publication.parse_obj(response)

        # Assert
        assert status == expected_status[AllowedMethod.GET]
        assert software.title == "test"
        assert software.xdd_uri == "fake"

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

    def test_rest_delete(self):
        # Act
        _, delete_status = self.fetch("/external/software/1", AllowedMethod.DELETE)
        _, retrieve_status = self.fetch("/external/software/1")

        # Assert
        assert delete_status == expected_status[AllowedMethod.DELETE]
        assert retrieve_status == 404
