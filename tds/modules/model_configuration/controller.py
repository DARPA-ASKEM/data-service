"""
TDS Model Configuration Controller
"""
from logging import Logger

from elasticsearch import NotFoundError
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tds.db import es_client
from tds.modules.model_configuration.model import ModelConfiguration
from tds.modules.model_configuration.response import (
    ModelConfigurationResponse,
    configuration_response,
)
from tds.operation import create, delete, retrieve, update

model_configuration_router = APIRouter()
logger = Logger(__name__)
es_index = ModelConfiguration.index


@model_configuration_router.get(
    "",
    response_model=list[ModelConfigurationResponse],
    **retrieve.fastapi_endpoint_config,
)
def list_model_configurations(page_size: int = 100, page: int = 0) -> JSONResponse:
    """
    Retrieve the list of model_configurations from ES.
    """
    es = es_client()
    list_body = {
        "size": page_size,
        # "fields": [],
        "from_": page,
    }
    res = es.search(index=es_index, **list_body)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=jsonable_encoder(configuration_response(res["hits"]["hits"])),
    )


@model_configuration_router.post("", **create.fastapi_endpoint_config)
def model_configuration_post(payload: ModelConfiguration) -> JSONResponse:
    """
    Create model_configuration and return its ID
    """
    res = payload.save()
    logger.info("New model_configuration created: %s", res["_id"])
    return JSONResponse(
        status_code=200,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@model_configuration_router.get(
    "/{model_configuration_id}",
    response_model=ModelConfigurationResponse,
    **retrieve.fastapi_endpoint_config,
)
def model_configuration_get(model_configuration_id: str | int) -> JSONResponse:
    """
    Retrieve a model_configuration from ElasticSearch
    """
    try:
        es = es_client()
        res = es.get(index=es_index, id=model_configuration_id)
        logger.info("ModelConfiguration retrieved: %s", model_configuration_id)
        source = res["_source"]
        source["id"] = res["_id"]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(ModelConfigurationResponse(**res["_source"])),
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
) -> JSONResponse:
    """
    Update a model_configuration in ElasticSearch
    """
    if payload.id != model_configuration_id:
        raise HTTPException(
            status_code=422, detail="ID in request URL and in payload must match."
        )
    res = payload.save(model_configuration_id)
    logger.info("model_configuration updated: %s", model_configuration_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@model_configuration_router.delete(
    "/{model_configuration_id}", **delete.fastapi_endpoint_config
)
def model_configuration_delete(model_configuration_id: str | int) -> Response:
    """
    Function deletes a model_configuration in ES.
    """
    try:
        es = es_client()
        res = es.delete(index=es_index, id=model_configuration_id)

        if res["result"] != "deleted":
            logger.error(
                "Failed to delete model_configuration: %s", model_configuration_id
            )
            raise Exception(
                f"Failed to delete  Model Configuration. ElasticSearch Response: "
                f"{res['result']}",
            )

        logger.info(
            "ModelConfiguration successfully deleted: %s", model_configuration_id
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
