"""
TDS Model Utils

Module provides basic utilities to handle model logic like
response form.
"""
from typing import List

import pandas as pd
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from tds.db.relational import engine as pg_engine
from tds.modules.model.model import ModelFramework
from tds.modules.model.model_description import ModelDescription

model_list_fields = [
    "id",
    "header",
    "name",
    "model",
    "description",
    "schema",
    "schema_name",
    "model_version",
    "timestamp",
]


def orm_to_params(parameters: List):
    """
    Convert SQL parameter search to dict
    """
    return [
        {
            "id": param.id,
            "name": param.name,
            "type": jsonable_encoder(param.type),
            "default_value": param.default_value,
            "state_variable": param.state_variable,
        }
        for param in parameters
    ]


def restructure_model_header(model: dict) -> dict:
    """
    Restructures the Model data by moving specific keys into the 'header' sub-dictionary.
    This makes all seeds and prior models comply with https://github.com/DARPA-ASKEM/Model-Representations/issues/56
    Parameters:
    - model (dict): The original Model data.
    Returns:
    - dict: The restructured Model data.
    """

    if "header" not in model:
        # The keys to be moved to the 'header'
        header_keys = [
            "name",
            "description",
            "model_schema",
            "schema",
            "schema_name",
            "model_version",
        ]

        # Create the 'header' sub-dictionary
        header_data = {key: model.pop(key) for key in header_keys if key in model}

        # Add the 'header' sub-dictionary to the original data
        model["header"] = header_data

    # Rename 'schema' to 'model_schema' if present
    if "model_schema" in model["header"]:
        schema = model["header"].pop("model_schema")
        if "schema" not in model["header"]:
            model["header"]["schema"] = schema

    return model


def model_response(model_from_es, delete_fields=None) -> dict:
    """
    Function builds model response object from an ElasticSearch model.
    """
    es_response = model_from_es.body
    model = es_response["_source"]
    # model["state_id"] = es_response["_id"]
    # frameworks = get_frameworks()
    # model["framework"] = frameworks.get(model["model_schema"], model["model_schema"])

    model = restructure_model_header(model)

    if "concepts" in model:
        del model["concepts"]

    if delete_fields and delete_fields is List:
        for field in delete_fields:
            del model[field]

    return model


def model_list_response(model_list_from_es) -> list:
    """
    Function builds model response object from an ElasticSearch model.
    """

    models = []
    for model_obj in model_list_from_es:
        if "_source" in model_obj:
            model_dict = restructure_model_header(model_obj["_source"])
        elif "fields" in model_obj:
            # Reformat fields to what it should look like
            field_dict = {
                k: (v[0] if (isinstance(v, list) and len(v) == 1) else v)
                for k, v in model_obj["fields"].items()
            }
            model_dict = restructure_model_header(field_dict)
        models.append(jsonable_encoder(ModelDescription(**model_dict)))
    return models


def get_frameworks() -> dict:
    """
    Get model frameworks from postgres.
    """
    with Session(pg_engine) as pg_db:
        frameworks = pg_db.query(ModelFramework).all()
        framework_map = {}
        for framework in frameworks:
            framework_map[framework.schema_url] = framework.name
    return framework_map
