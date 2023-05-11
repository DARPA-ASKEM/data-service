import json
from logging import Logger
from pprint import pprint
from typing import List, Optional

from elasticsearch import NotFoundError
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.db import es
from tds.modules.model.model import Model
from tds.modules.model.utils import model_list_response, model_response
from tds.operation import create, delete, retrieve, update

model_router = APIRouter()
logger = Logger(__name__)


@model_router.get("/descriptions", **retrieve.fastapi_endpoint_config)
def list_models(page_size: int = 100, page: int = 0) -> List:
    """
    Retrieve the list of models from ES.
    """
    list_body = {
        "size": page_size,
        "fields": ["name", "description", "model_schema", "model_version"],
        "_source": False,
    }
    if page != 0:
        list_body["from"] = page
    res = es.search(index="model", body=list_body)

    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=model_list_response(res["hits"]["hits"]),
    )


@model_router.post("", **create.fastapi_endpoint_config)
def model_post(payload: Model) -> Response:
    """
    Create model and return its ID
    """
    res = payload.save()
    logger.info(f"new model created: {id}")
    return Response(
        status_code=200,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": res["_id"]}),
    )


@model_router.get("/{id}", **retrieve.fastapi_endpoint_config)
def model_get(id: str | int) -> Response:
    """
    Retrieve a model from ElasticSearch
    """
    try:
        res = es.get(index="model", id=id)
        pprint(res)
        logger.info(f"model retrieved: {id}")

        return Response(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=json.dumps(model_response(res)),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@model_router.put("/{id}", **update.fastapi_endpoint_config)
def model_put(id: str | int, payload: Model) -> Response:
    """
    Update a model in ElasticSearch
    """
    res = payload.save(id)
    logger.info("model updated: %i", id)
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": res["_id"]}),
    )


@model_router.delete("/{id}", **delete.fastapi_endpoint_config)
def model_delete(id: str | int) -> Response:
    try:
        res = es.delete(index="model", id=id)

        if res["result"] != "deleted":
            logger.error(f"Failed to delete model: {id}")
            raise Exception(
                f"Failed to delete model. ElasticSearch Response: {res['result']}"
            )

        logger.info(f"Model successfully deleted: {id}")
        return Response(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )
