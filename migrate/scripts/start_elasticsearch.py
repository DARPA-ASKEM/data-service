#!/usr/bin/env python
import json
import os

from elasticsearch import Elasticsearch

ES_URL = os.getenv("ES_URL")
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")
ES_INDEX_PREFIX = os.getenv("ES_INDEX_PREFIX")


def setup_elasticsearch_indexes() -> None:
    """
    Function creates indexes in ElasticSearch.
    """
    es = Elasticsearch([ES_URL], basic_auth=(ES_USERNAME, ES_PASSWORD))
    # Config should match keyword args on
    # https://elasticsearch-py.readthedocs.io/en/v8.3.2/api.html#elasticsearch.client.IndicesClient.create
    with open("/migrate/indexes.json", "r") as index_file:
        indices = json.load(index_file)

        # Create indexes
        for idx, config in indices.items():
            index_name = f"{ES_INDEX_PREFIX}{idx}"
            print(f"Checking {index_name}")
            if not es.indices.exists(index=index_name):
                print(f"Creating {index_name} index.")
                # logger.debug("Creating index %s", index_name)
                es.indices.create(index=index_name, mappings=config)


if __name__ == "__main__":
    print("Checking Elastic Search.")
    setup_elasticsearch_indexes()
