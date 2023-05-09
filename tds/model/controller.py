import json
from pprint import pprint

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.db import es
from tds.model.model import Model
from tds.operation import create

router = APIRouter()
route_prefix = "mdl"


@router.post("", **create.fastapi_endpoint_config)
def model_post(payload: Model) -> Response:
    """
    Create model and return its ID
    """
    res = es.index(index="model", body=payload.dict())

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": res["_id"]}),
    )
