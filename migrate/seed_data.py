#!/usr/bin/env python
import json
import os

from elasticsearch import ConflictError, Elasticsearch

ES_URL = os.getenv("ES_URL")
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")
ES_INDEX_PREFIX = os.getenv("ES_INDEX_PREFIX")

es = Elasticsearch([ES_URL], basic_auth=(ES_USERNAME, ES_PASSWORD))

migrate_dir = os.path.dirname(__file__)
seed_dir = f"{migrate_dir}/seeds"
es_seed_dir = f"{seed_dir}/es"


def seed_es_data():
    print("Seeding ElasticSearch Data.")
    for directory in os.listdir(es_seed_dir):
        path_dir = f"{es_seed_dir}/{directory}"
        for file in os.listdir(path_dir):
            file_path = f"{path_dir}/{file}"
            with open(file_path, "r") as es_file_data:
                save_data_to_es(directory=directory, data=es_file_data)


def seed_postgres_data():
    print("Seeding Postgres Data.")


def save_data_to_es(directory, data):
    index = f"{ES_INDEX_PREFIX}{directory}"
    data_dict = json.load(data)
    try:
        res = es.create(index=index, document=data_dict, id=data_dict["id"])
        if res["result"] != "created":
            print(res)
    except ConflictError as e:
        fail_id = data_dict["id"]
        print(f"Item with id {fail_id} already exists in {index}. ({e.status_code})")


if __name__ == "__main__":
    # Seed ES first so we have the IDs for provenance.
    seed_es_data()
    seed_postgres_data()
