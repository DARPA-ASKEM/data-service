"""
TDS Model Controller.
"""
import json
from logging import Logger
from typing import List

from elasticsearch import NotFoundError
from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

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
        "source": False,
    }
    if page != 0:
        list_body["from"] = page
    res = es.search(index="model", **list_body)
    print(res)

    list_body = model_list_response(res["hits"]["hits"]) if res["hits"]["hits"] else []

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=list_body,
    )


@model_router.post("", **create.fastapi_endpoint_config)
def model_post(payload: Model) -> JSONResponse:
    """
    Create model and return its ID
    """
    res = payload.save()
    logger.info("new model created: %s", res["_id"])
    return JSONResponse(
        status_code=200,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@model_router.get("/{model_id}/descriptions", **retrieve.fastapi_endpoint_config)
def model_descriptions_get(model_id: str | int) -> JSONResponse | Response:
    """
    Retrieve a model 'description' from ElasticSearch
    """
    try:
        res = es.get(index="model", id=model_id)
        logger.info("model retrieved for description: %s", model_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=model_response(res, delete_fields=["model", "model_version"]),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@model_router.get("/{model_id}/parameters", **retrieve.fastapi_endpoint_config)
def model_parameters_get(model_id: str | int) -> JSONResponse | Response:
    """
    Function retrieves a Model's parameters.
    """
    try:
        res = es.get(index="model", id=model_id, source_includes=["model.parameters"])
        logger.info("model retrieved for params: %s", model_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=res["_source"]["model"]["parameters"],
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@model_router.get("/{model_id}", **retrieve.fastapi_endpoint_config)
def model_get(model_id: str | int) -> JSONResponse | Response:
    """
    Retrieve a model from ElasticSearch
    """
    try:
        res = es.get(index="model", id=model_id)
        logger.info("model retrieved: %s", model_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=model_response(res),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@model_router.put("/{model_id}", **update.fastapi_endpoint_config)
def model_put(model_id: str | int, payload: Model) -> JSONResponse:
    """
    Update a model in ElasticSearch
    """
    res = payload.save(model_id)
    logger.info("model updated: %s", model_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@model_router.delete("/{model_id}", **delete.fastapi_endpoint_config)
def model_delete(model_id: str | int) -> Response:
    """
    Function deletes a TDS Model from ElasticSearch.
    """
    try:
        res = es.delete(index="model", id=model_id)

        if res["result"] != "deleted":
            logger.error("Failed to delete model: %s", model_id)
            raise Exception(
                f"Failed to delete model. ElasticSearch Response: {res['result']}"
            )

        logger.info("Model successfully deleted: %s", model_id)
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
