import os

import boto3
import elasticsearch
from elasticsearch import Elasticsearch
from fastapi.testclient import TestClient
from moto import mock_s3
from pytest import fixture
from pytest_elasticsearch import factories

from tds.server.build import build_api

os.environ["TDS_HOST_PORT"] = "8888"
os.environ["SQL_URL"] = "localhost"
os.environ["SQL_PORT"] = "5432"
os.environ["SQL_USER"] = "dev"
os.environ["SQL_PASSWORD"] = "dev"
os.environ["SQL_DB"] = "askem"
os.environ["DKG_URL"] = "http://dpk"
os.environ["DKG_API_PORT"] = "8771"
os.environ["DKG_DESC_PORT"] = "8772"
os.environ["S3_BUCKET"] = "test-data-service-data"
os.environ["S3_DATASET_PATH"] = "test-datasets"
os.environ["S3_RESULTS_PATH"] = "test-simulations"
os.environ["S3_ARTIFACT_PATH"] = "test-artifacts"
os.environ["STORAGE_HOST"] = "http://test-minio:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "askem-s3-test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testPass"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["ES_URL"] = "http://test-es:9200"
os.environ["ES_HOST"] = "test-es"
os.environ["ES_PORT"] = "9200"


@fixture(autouse=True)
def s3_fixture():
    mock_s3().start()
    resource = boto3.resource("s3", region_name="us-east-1")

    # Create the table
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


@fixture(autouse=True)
def _mock_elasticsearch():
    # mocker.object.patch(Elasticsearch, "search")
    elasticsearch_proc = factories.elasticsearch_proc(
        host=os.getenv("ES_HOST"),
        port=os.getenv("9200"),
        network_publish_host=os.getenv("ES_HOST"),
    )
    yield elasticsearch_proc
