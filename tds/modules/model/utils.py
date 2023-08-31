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

    model_df = pd.DataFrame(model_list_from_es)
    # framework_map = get_frameworks()
    # We need to get the fields and then merge back to make the id available.
    models = (
        pd.concat({i: pd.DataFrame(x) for i, x in model_df.pop("fields").items()})
        .reset_index(level=1, drop=True)
        .join(model_df)
        .reset_index(drop=True)
    )

    models["model_version"] = models["model_version"].fillna(0)

    models.drop(columns=["_index", "_score"], inplace=True)

    # Drop _ignored column when it is present.
    if "_ignored" in models.columns:
        models.drop(columns=["_ignored"], inplace=True)

    return [
        jsonable_encoder(ModelDescription(**restructure_model_header(x)))
        for x in models.to_dict(orient="records")
    ]


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
