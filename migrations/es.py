"""
Elasticsearch functions and helpers useful for migrations
"""

from tds.db.elasticsearch import es_client

es = es_client()


def create_index(index_name, schema=None, **extra_options):
    try:
        result = es.indices.create(index=index_name, mappings=schema, **extra_options)
    except:
        # TODO: Better error handling
        raise


def retrieve_index_schema(index_name):
    return es.indices.get_mapping(index=index_name)


def update_index_schema(index_name, new_schema, old_schema=None):
    current_schema = retrieve_index_schema(index_name)
    if old_schema is not None:
        if current_schema != old_schema:
            raise ValueError(
                "Provided schema does not match the expected current state."
            )
    temp_index = f"temp_{index_name}"
    create_index(temp_index, current_schema)
    es.reindex(source=index_name, dest=temp_index)
    remove_index(index_name)
    create_index(index_name, schema=new_schema)
    es.reindex(source=temp_index, dest=index_name)
    remove_index(temp_index)


def remove_index(index_name):
    es.indices.delete(index=index_name)


def truncate_index(index_name):
    schema = retrieve_index_schema(index_name)
    settings = es.indices.get_settings(index=index_name)
    remove_index(index_name)
    es.indices.create(index=index_name, mappings=schema, settings=settings)


def bulk_load_index_from_jsonl(index_name, jsonl_file_path):
    pass
