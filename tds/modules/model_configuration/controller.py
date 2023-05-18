import json
from logging import Logger
from typing import List

from elasticsearch import NotFoundError
from fastapi import APIRouter, Depends, HTTPException, Response, status

from tds.db import es
from tds.modules.model_configuration.model import ModelConfiguration
from tds.operation import create, delete, retrieve, update

model_configuration_router = APIRouter()
logger = Logger(__name__)


@model_configuration_router.get("", **retrieve.fastapi_endpoint_config)
def list_model_configurations(page_size: int = 100, page: int = 0) -> List:
    """
    Retrieve the list of model_configurations from ES.
    """
    list_body = {
        "size": page_size,
        # "fields": [], --** This option allows you to select specific fields from ES **--
        "_source": False,
    }
    if page != 0:
        list_body["from"] = page
    res = es.search(index="model_configuration", body=list_body)

    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps(res["hits"]["hits"]),
    )


@model_configuration_router.post("", **create.fastapi_endpoint_config)
def model_configuration_post(payload: ModelConfiguration) -> Response:
    """
    Create model_configuration and return its ID
    """
    res = payload.save()
    logger.info(f"New model_configuration created: {id}")
    return Response(
        status_code=200,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": res["_id"]}),
    )


@model_configuration_router.get(
    "/{model_configuration_id}", **retrieve.fastapi_endpoint_config
)
def model_configuration_get(model_configuration_id: str | int) -> Response:
    """
    Retrieve a model_configuration from ElasticSearch
    """
    try:
        res = es.get(index="model_configuration", id=model_configuration_id)
        logger.info(f"ModelConfiguration retrieved: {model_configuration_id}")

        return Response(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=json.dumps(res),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@model_configuration_router.put(
    "/{model_configuration_id}", **update.fastapi_endpoint_config
)
def model_configuration_put(
    model_configuration_id: str | int, payload: ModelConfiguration
) -> Response:
    """
    Update a model_configuration in ElasticSearch
    """
    res = payload.save(model_configuration_id)
    logger.info(f"model_configuration updated: {model_configuration_id}")
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": res["_id"]}),
    )


@model_configuration_router.delete(
    "/{model_configuration_id}", **delete.fastapi_endpoint_config
)
def model_configuration_delete(model_configuration_id: str | int) -> Response:
    try:
        res = es.delete(index="model_configuration", id=model_configuration_id)

        if res["result"] != "deleted":
            logger.error(
                f"Failed to delete model_configuration: {model_configuration_id}"
            )
            raise Exception(
                f"Failed to delete  Model Configuration. ElasticSearch Response: {res['result']}"
            )

        logger.info(
            f"ModelConfiguration successfully deleted: {model_configuration_id}"
        )
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
