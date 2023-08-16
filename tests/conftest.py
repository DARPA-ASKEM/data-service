import os

import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_s3
from pytest import fixture

from tds.server.build import build_api


def pytest_configure():
    pytest.model_id = None
    pytest.project_id = None
    pytest.model_configuration_id = None
    pytest.workflow_id = None
    pytest.code_id = None


@fixture(autouse=True)
def s3_fixture():
    mock_s3().start()
    resource = boto3.resource("s3", region_name="us-east-1")

    # Create the s3 bucket.
    resource.create_bucket(Bucket=os.getenv("S3_BUCKET"))
    yield resource

    mock_s3().stop()


@fixture(autouse=True)
def fast_api_fixture():
    fast_api = build_api()
    yield TestClient(fast_api)


@fixture(autouse=True)
def fast_api_test_url():
    port = os.getenv("TDS_HOST_PORT")
    return f"http://localhost:{port}"
