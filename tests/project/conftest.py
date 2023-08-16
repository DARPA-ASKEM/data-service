import pytest
from pytest import fixture


@fixture()
def project_json():
    return {
        "name": "A cool project",
        "description": "Project info goes here.",
        "assets": {},
        "active": "true",
        "username": "Loki",
    }
