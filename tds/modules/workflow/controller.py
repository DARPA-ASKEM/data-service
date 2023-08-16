"""
    TDS Workflow Controller.

    Description: Defines the basic rest endpoints for the TDS Module.
"""
from logging import Logger

from elasticsearch import NotFoundError
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tds.db import es_client
from tds.modules.workflow.model import Workflow
from tds.modules.workflow.response import WorkflowResponse, workflow_response
from tds.operation import create, delete, retrieve, update

workflow_router = APIRouter()
logger = Logger(__name__)
es_index = Workflow.index


@workflow_router.get(
    "", response_model=list[WorkflowResponse], **retrieve.fastapi_endpoint_config
)
def list_workflows(page_size: int = 100, page: int = 0) -> JSONResponse:
    """
    Retrieve the list of workflows from ES.
    """
    es = es_client()
    list_body = {"size": page_size, "from_": page}

    res = es.search(index=es_index, **list_body)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=jsonable_encoder(workflow_response(res["hits"]["hits"])),
    )


@workflow_router.post("", **create.fastapi_endpoint_config)
def workflow_post(payload: Workflow) -> JSONResponse:
    """
    Create workflow and return its ID
    """
    res = payload.save()
    logger.info("New workflow created: %s", res["_id"])
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@workflow_router.get(
    "/{workflow_id}",
    response_model=WorkflowResponse,
    **retrieve.fastapi_endpoint_config,
)
def workflow_get(workflow_id: str) -> JSONResponse | Response:
    """
    Retrieve a workflow from ElasticSearch
    """
    try:
        es = es_client()
        res = es.get(index=es_index, id=workflow_id)
        logger.info("Workflow retrieved: %s", workflow_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(res["_source"]),
        )
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@workflow_router.put("/{workflow_id}", **update.fastapi_endpoint_config)
def workflow_put(workflow_id: str, payload: Workflow) -> JSONResponse | Response:
    """
    Update a workflow in ElasticSearch
    """
    try:
        res = payload.save()
        logger.info("workflow updated: %s", res["_id"])
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content={"id": workflow_id},
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@workflow_router.delete("/{workflow_id}", **delete.fastapi_endpoint_config)
def workflow_delete(workflow_id: str) -> Response:
    """
    Delete a Workflow in ElasticSearch
    """
    try:
        es = es_client()
        res = es.delete(index=es_index, id=workflow_id)

        if res["result"] != "deleted":
            logger.error("Failed to delete Workflow: %s", workflow_id)
            raise Exception(
                f"Failed to delete Workflow. ElasticSearch Response: {res['result']}"
            )

        logger.info("Workflow successfully deleted: %s", workflow_id)
        return Response(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
        )
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
