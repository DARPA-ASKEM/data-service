"""Prepopulate data from seed files

Revision ID: 030bffd9ef5a
Revises: b3bdf1b266ff
Create Date: 2023-09-21 17:03:41.966060

"""
import json
import os
from collections import OrderedDict

import sqlalchemy as sa

# pylint: disable=no-member, invalid-name
from alembic import op
from elasticsearch.exceptions import NotFoundError
from sqlalchemy.orm import Session

# Elasticsearch operators such as es.create_index, es.remove_index, es.update_index_schema, es.bulk_load_index_from_jsonl, etc
from migrations import es, storage
from tds.db.base import Base
from tds.settings import settings

# from migrations.env import target_metadata


# revision identifiers, used by Alembic.
revision = "030bffd9ef5a"
down_revision = "b3bdf1b266ff"
branch_labels = None
depends_on = None

es_seed_dir = os.path.abspath("migrations/seeds/es")
file_dir = os.path.abspath("migrations/seeds/files")


def upgrade() -> None:
    target_metadata = Base.metadata
    # Add Elasticsearch seed documents
    for index, file_path in es_seeds():
        data = json.load(open(file_path))
        try:
            es.add_seed_document(index_name=index, document=data)
        except Exception as e:
            print(e)

    # Add records to the RDB
    for table_name, records in rdb_records.items():
        table = sa.Table(table_name, target_metadata, autoload=True)
        op.bulk_insert(table=table, rows=records)

    s3_client = storage.create_s3_client()
    for filename, storage_info in datasets_to_store.items():
        storage_path = storage_info.get("storage_path")
        url = storage_info.get("url")
        file_path = os.path.join(file_dir, filename)
        full_storage_path = os.path.join(settings.S3_DATASET_PATH, storage_path)
        storage.download_file(url, file_path)
        storage.upload_file(s3_client, file_path, full_storage_path)


def downgrade() -> None:
    # Remove installed elasticsearch seed documents
    for index, file_path in es_seeds():
        data = json.load(open(file_path))
        document_id = data.get("id", None)
        if document_id:
            try:
                es.es.delete(index=index, id=document_id)
            except NotFoundError:
                pass

    # Remove seeded RDB records
    for table_name, records in reversed(rdb_records.items()):
        for record in records:
            conditional = " AND ".join(
                [f""""{key}" = '{value}'""" for key, value in record.items()]
            )
            statement = f"""DELETE FROM {table_name} WHERE {conditional}"""
            op.execute(statement)


def es_seeds():
    """
    Generator to iterate over all of the seeds for es
    """
    seed_dir = os.path.abspath("migrations/seeds/es")
    for dir in os.listdir(seed_dir):
        subdir = os.path.join(seed_dir, dir)
        if not os.path.isdir(subdir):
            continue
        for file_name in os.listdir(subdir):
            index = es.normalize_index(dir)
            file_path = os.path.join(subdir, file_name)
            yield index, file_path


# Order matters for adding and removing when there are references between the records
rdb_records = OrderedDict(
    [
        (
            "person",
            [
                {
                    "name": "Adam Ant",
                    "org": "Adam and the Ants",
                    "email": "adam@test.io",
                    "website": "http://www.adam-ant.com/",
                    "is_registered": True,
                },
            ],
        ),
        (
            "project",
            [
                {
                    "id": 1,
                    "name": "ASKEM Demo Project",
                    "description": "The ASKEM Demo Project",
                    "active": True,
                },
                {
                    "id": 2,
                    "name": "Another COVID-19 Modeling",
                    "description": "A project around modeling COVID-19.",
                    "active": True,
                },
            ],
        ),
        (
            "project_asset",
            [
                {
                    "project_id": 1,
                    "resource_id": "state-var-data-stage-3",
                    "resource_type": "datasets",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "covid-19-us-data",
                    "resource_type": "datasets",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "truth-incident-case",
                    "resource_type": "datasets",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "truth-incident-hospitalization",
                    "resource_type": "datasets",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "truth-incident-death",
                    "resource_type": "datasets",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "biomd0000000294-model-id",
                    "resource_type": "models",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "biomd0000000294-model-config-id",
                    "resource_type": "model_configurations",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "sir-model-id",
                    "resource_type": "models",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "biomd0000000983-model-id",
                    "resource_type": "models",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "biomd0000000960-model-id",
                    "resource_type": "models",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "biomd0000000955-model-id",
                    "resource_type": "models",
                    "external_ref": "object",
                },
                {
                    "project_id": 1,
                    "resource_id": "sir-model-config-id",
                    "resource_type": "model_configurations",
                    "external_ref": "object",
                },
            ],
        ),
        (
            "provenance",
            [
                {
                    "relation_type": "EXTRACTED_FROM",
                    "left": "sir-model-id",
                    "left_type": "Model",
                    "right": "1",
                    "right_type": "Publication",
                },
                {
                    "relation_type": "USES",
                    "left": "sir-model-config-id",
                    "left_type": "ModelConfiguration",
                    "right": "sir-model-id",
                    "right_type": "Model",
                },
            ],
        ),
        (
            "publication",
            [
                {
                    "xdd_uri": "xdd_url_for_publication",
                    "title": "This is a great paper.",
                },
                {
                    "xdd_uri": "xdd_url_for_publication_2",
                    "title": "This is another great paper.",
                },
            ],
        ),
    ]
)


datasets_to_store = {
    "us.csv": {
        "storage_path": "covid-19-us-data/us.csv",
        "url": "https://raw.githubusercontent.com/DARPA-ASKEM/experiments/blob/main/thin-thread-examples/milestone_6month/evaluation/ta1/usa-IRDVHN_age.csv",
    },
    "usa-IRDVHN_age.csv": {
        "storage_path": "state-var-data-stage-3/usa-IRDVHN_age.csv",
        "url": "https://raw.githubusercontent.com/nytimes/covid-19-data/blob/master/us.csv",
    },
    "truth-Incident Cases.csv": {
        "storage_path": "truth-incident-case/truth-Incident Cases.csv",
        "url": "https://media.githubusercontent.com/media/reichlab/covid19-forecast-hub/master/data-truth/truth-Incident%20Cases.csv",
    },
    "truth-Incident Deaths.csv": {
        "storage_path": "truth-incident-death/truth-Incident Deaths.csv",
        "url": "https://media.githubusercontent.com/media/reichlab/covid19-forecast-hub/master/data-truth/truth-Incident%20Deaths.csv",
    },
    "truth-Incident Hospitalizations.csv": {
        "storage_path": "truth-incident-hospitalization/truth-Incident Hospitalizations.csv",
        "url": "https://media.githubusercontent.com/media/reichlab/covid19-forecast-hub/master/data-truth/truth-Incident%20Hospitalizations.csv",
    },
}
