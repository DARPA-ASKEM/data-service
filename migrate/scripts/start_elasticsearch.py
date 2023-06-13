#!/usr/bin/env python
"""
Elasticsearch data module.
"""
import json
import os
import sys
from pathlib import Path

from elasticsearch import ConflictError, Elasticsearch

ES_URL = os.getenv("ES_URL")
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")
ES_INDEX_PREFIX = os.getenv("ES_INDEX_PREFIX")

migrate_dir = Path(os.path.dirname(__file__))
seed_dir = f"{migrate_dir.parent}/seeds"
es_seed_dir = f"{seed_dir}/es"
es = Elasticsearch([ES_URL], basic_auth=(ES_USERNAME, ES_PASSWORD))


def setup_elasticsearch_indexes() -> None:
    """
    Function creates indexes in ElasticSearch.
    """
    # Config should match keyword args on
    # https://elasticsearch-py.readthedocs.io/en/v8.3.2/api.html#elasticsearch.client.IndicesClient.create
    with open(f"{es_seed_dir}/indexes.json", "r", encoding="utf-8") as index_file:
        indices = json.load(index_file)

        # Create indexes
        for idx, config in indices.items():
            index_name = f"{ES_INDEX_PREFIX}{idx}"
            print(f"Checking {index_name}")
            if not es.indices.exists(index=index_name):
                print(f"Creating {index_name} index.")
                # logger.debug("Creating index %s", index_name)
                es.indices.create(index=index_name, mappings=config)


def save_data_to_es(directory, data):
    """
    Function saves data to ES.
    """

    index = f"{ES_INDEX_PREFIX}{directory}"
    data_dict = json.load(data)
    try:
        res = es.create(index=index, document=data_dict, id=data_dict["id"])
        if res["result"] != "created":
            print(res)
        else:
            name = data_dict["name"]
            print(f"Created {name}.")
    except ConflictError as error:
        fail_id = data_dict["id"]
        print(
            f"Item with id {fail_id} already exists in {index}. ({error.status_code})"
        )


def seed_es_data():
    """
    Function seeds data into ES.
    """
    print("Seeding ElasticSearch Data.")
    for directory in os.listdir(es_seed_dir):
        path_dir = f"{es_seed_dir}/{directory}"
        if os.path.isfile(path_dir):
            continue
        for file in os.listdir(path_dir):
            file_path = f"{path_dir}/{file}"
            with open(file_path, "r", encoding="utf-8") as es_file_data:
                save_data_to_es(directory=directory, data=es_file_data)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        seed_es_data()
    else:
        print("Checking Elastic Search.")
        setup_elasticsearch_indexes()
