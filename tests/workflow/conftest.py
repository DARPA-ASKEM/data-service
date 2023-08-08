from pytest import fixture


@fixture()
def workflow_json():
    return {
        "name": "Test Workflow",
        "description": "This is the description",
        "edges": [{"id": "edge"}],
        "transform": {"x": 124.932, "y": 48.65, "k": 3.1},
        "nodes": [],
    }
