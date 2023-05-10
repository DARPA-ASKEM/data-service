import json
from logging import Logger
from pprint import pprint
from typing import Optional

from elasticsearch import NotFoundError
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.db import es
from tds.model.model import Model
from tds.operation import create, retrieve, update

logger = Logger(__name__)
router = APIRouter()
route_prefix = "mdl"


@router.post("", **create.fastapi_endpoint_config)
def model_post(payload: Model) -> Response:
    """
    Create model and return its ID
    """
    res = es.index(index="model", body=payload.dict())
    logger.info("new model created: %i", id)
    return Response(
        status_code=200,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": res["_id"]}),
    )


@router.get("/{id}", **retrieve.fastapi_endpoint_config)
def model_get(id: str | int) -> Response:
    """
    Retrieve a model from ElasticSearch
    """
    try:
        res = es.get(index="model", id=id)
        logger.info("model retrieved: %i", id)

        return Response(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=json.dumps(res["_source"]),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@router.put("/{id}", **update.fastapi_endpoint_config)
def model_put(id: str | int, payload: Model) -> Response:
    """
    Update a model in ElasticSearch
    """
    res = es.index(index="model", body=payload.dict(), id=id)
    logger.info("model updated: %i", id)
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": res["_id"]}),
    )
