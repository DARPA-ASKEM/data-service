from typing import List

import pandas as pd
from sqlalchemy.orm import Query, Session

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


def model_response(model_from_es):
    """
    Function builds model response object from an ElasticSearch model.
    """
    es_response = model_from_es.body
    model = es_response["_source"]
    model["id"] = es_response["_id"]
    del model["concepts"]

    return model


def model_list_response(model_list_from_es):
    """
    Function builds model response object from an ElasticSearch model.
    """
    df = pd.DataFrame(model_list_from_es)
    fields = pd.json_normalize(df["fields"])
    with Session(pg_engine) as pg_db:
        frameworks = pg_db.query(orm.ModelFramework).all()
        framework_map = {}
        for f in frameworks:
            framework_map[f.schema_url] = f.name

    for col in fields.columns:
        fields[col] = fields[col].map(lambda x: x[0])
        if col == "model_schema":
            fields["framework"] = fields[col].map(lambda x: framework_map[x])

    return fields.to_json(orient="records")
