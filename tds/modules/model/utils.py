"""
TDS Model Utils

Module provides basic utilities to handle model logic like
response form.
"""
from typing import List

import pandas as pd
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db.relational import engine as pg_engine


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


def model_response(model_from_es, delete_fields=None) -> dict:
    """
    Function builds model response object from an ElasticSearch model.
    """
    es_response = model_from_es.body
    model = es_response["_source"]
    model["state_id"] = model["id"] = es_response["_id"]
    frameworks = get_frameworks()
    model["framework"] = frameworks[model["model_schema"]]
    model["schema"] = model["model_schema"]

    del model["model_schema"]
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
    framework_map = get_frameworks()
    # We need to get the fields and then merge back to make the id available.
    models = (
        pd.concat({i: pd.DataFrame(x) for i, x in model_df.pop("fields").items()})
        .reset_index(level=1, drop=True)
        .join(model_df)
        .reset_index(drop=True)
    )

    # we should use the same terminology here as is used in the ASKEM model
    # representation e.g. instead of `model_schema` that should just be `schema`
    models["framework"] = models["model_schema"].map(lambda x: framework_map[x])
    models.rename(columns={"_id": "id"}, inplace=True)
    models.drop(columns=["_index", "_score"], inplace=True)

    return models.to_json(orient="records")


def get_frameworks() -> dict:
    """
    Get model frameworks from postgres.
    """
    with Session(pg_engine) as pg_db:
        frameworks = pg_db.query(orm.ModelFramework).all()
        framework_map = {}
        for framework in frameworks:
            framework_map[framework.schema_url] = framework.name
    return framework_map
