"""
Elasticsearch functions and helpers useful for migrations
"""

from elasticsearch.exceptions import BadRequestError

from tds.db.elasticsearch import es_client
from tds.settings import settings

es = es_client()


def normalize_index(index_name: str):
    """
    Normalizes an index name, ensuring that the proper prefix is prepended if needed.
    You can pass in an index with or without the prefix.
    """
    if (
        index_name.startswith(settings.ES_INDEX_PREFIX)
        and index_name != settings.ES_INDEX_PREFIX
    ):
        return index_name
    else:
        return f"{settings.ES_INDEX_PREFIX}{index_name}"


def create_index(index_name: str, mapping=None, **extra_options):
    """
    Creates an index with the provided mapping/mappings.
    extra_options is passed to es.indices.create()
    """
    # TODO: Better error handling
    es.indices.create(index=index_name, mappings=mapping, **extra_options)


def retrieve_index_mapping(index_name: str):
    """
    Retrieve an index's mapping
    """
    return es.indices.get_mapping(index=index_name).get(index_name, {}).get("mappings")


def update_index_mapping(index_name: str, new_mapping):
    """
    Uses the ElasticSearch reindex functionality to update the mapping on an index.
    Basically moves the data twice, first to a temporary index without any mapping rules,
    then the original index is removed and recreated with the desired mapping and the
    records are moved to the recreated index to be mapped properly.
    """
    temp_index = f"temp_{index_name}"
    try:
        create_index(temp_index, {"enabled": False})
    except BadRequestError as err:
        # If the temporary index already exists, delete it and recreate so we can confirm
        # it is created correctly and empty.
        if err.error == "resource_already_exists_exception":
            print(f"Index {temp_index} already exists. Deleting and recreating.")
            remove_index(temp_index)
            create_index(temp_index, {"enabled": False})
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
    create_index(index_name, mapping=new_mapping)
    es.reindex(
        source={"index": temp_index},
        dest={"index": index_name},
        refresh=True,
        wait_for_completion=True,
        timeout="10m",
    )
    remove_index(temp_index)


def remove_index(index_name: str, **extra_args):
    """
    Remove the specified index
    """
    es.indices.delete(index=index_name, **extra_args)


def truncate_index(index_name: str):
    """
    Truncate the index by removing it and recreating it.
    """
    mapping = retrieve_index_mapping(index_name)
    index_settings = es.indices.get_settings(index=index_name)
    remove_index(index_name)
    es.indices.create(index=index_name, mappings=mapping, settings=index_settings)


def add_seed_document(index_name: str, document: dict):
    """
    Add a document as part of seeding Elasticsearch.
    """
    es.create(index=index_name, document=document, id=document.get("id", None))
