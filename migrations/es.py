"""
Elasticsearch functions and helpers useful for migrations
"""

from elasticsearch.exceptions import BadRequestError

from tds.db.elasticsearch import es_client
from tds.settings import settings

es = es_client()


def normalize_index(index_name: str):
    if (
        index_name.startswith(settings.ES_INDEX_PREFIX)
        and index_name != settings.ES_INDEX_PREFIX
    ):
        return index_name
    else:
        return f"{settings.ES_INDEX_PREFIX}{index_name}"


def create_index(index_name: str, schema=None, **extra_options):
    try:
        result = es.indices.create(index=index_name, mappings=schema, **extra_options)
    except:
        # TODO: Better error handling
        raise


def retrieve_index_schema(index_name: str):
    return es.indices.get_mapping(index=index_name).get(index_name, {}).get("mappings")


def update_index_schema(index_name: str, new_schema, old_schema=None):
    current_schema = retrieve_index_schema(index_name)
    if old_schema is not None:
        if current_schema != old_schema:
            raise ValueError(
                "Provided schema does not match the expected current state."
            )
    temp_index = f"temp_{index_name}"
    try:
        create_index(temp_index, {"enabled": False})
    except BadRequestError as err:
        # If the temporary index already exists, delete it and recreate so we can confirm
        # it is created correctly and empty.
        if err.error == "resource_already_exists_exception":
            print(f"Index {temp_index} already exists. Deleting and recreating.")
            remove_index(temp_index)
            create_index(temp_index, current_schema)
        else:
            raise
    es.reindex(
        source={"index": index_name},
        dest={"index": temp_index},
        refresh=True,
        wait_for_completion=True,
        timeout="10m",
    )
    remove_index(index_name, timeout="1m")
    create_index(index_name, schema=new_schema)
    es.reindex(
        source={"index": temp_index},
        dest={"index": index_name},
        refresh=True,
        wait_for_completion=True,
        timeout="10m",
    )
    remove_index(temp_index)


def remove_index(index_name: str, **extra_args):
    es.indices.delete(index=index_name, **extra_args)


def truncate_index(index_name: str):
    schema = retrieve_index_schema(index_name)
    settings = es.indices.get_settings(index=index_name)
    remove_index(index_name)
    es.indices.create(index=index_name, mappings=schema, settings=settings)


def add_seed_document(index_name: str, document: dict):
    es.create(index=index_name, document=document, id=document.get("id", None))
