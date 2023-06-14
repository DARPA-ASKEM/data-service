"""
    TDS Artifact Controller.

    Description: Defines the basic rest endpoints for the TDS Module.
"""
from logging import Logger

from elasticsearch import NotFoundError
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tds.db import es_client
from tds.modules.artifact.model import Artifact
from tds.modules.artifact.response import ArtifactResponse, artifact_response
from tds.operation import create, delete, retrieve, update

artifact_router = APIRouter()
logger = Logger(__name__)
es_index = Artifact.index


@artifact_router.get(
    "", response_model=list[ArtifactResponse], **retrieve.fastapi_endpoint_config
)
def list_artifacts(page_size: int = 100, page: int = 0) -> JSONResponse:
    """
    Retrieve the list of artifacts from ES.
    """
    es = es_client()
    list_body = {
        "size": page_size,
        # --** This option allows you to select specific fields from ES **--
        # "fields": [],
        "from_": page,
    }

    res = es.search(index=es_index, **list_body)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=jsonable_encoder(artifact_response(res["hits"]["hits"])),
    )


@artifact_router.post("", **create.fastapi_endpoint_config)
def artifact_post(payload: Artifact) -> JSONResponse:
    """
    Create artifact and return its ID
    """
    res = payload.save()
    logger.info("New artifact created: %s", res["_id"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@artifact_router.get(
    "/{artifact_id}",
    response_model=ArtifactResponse,
    **retrieve.fastapi_endpoint_config,
)
def artifact_get(artifact_id: str) -> JSONResponse | Response:
    """
    Retrieve a artifact from ElasticSearch
    """
    try:
        es = es_client()
        res = es.get(index=es_index, id=artifact_id)
        logger.info("Artifact retrieved: %s", artifact_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(ArtifactResponse(**res["_source"])),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@artifact_router.put("/{artifact_id}", **update.fastapi_endpoint_config)
def artifact_put(artifact_id: str, payload: Artifact) -> JSONResponse | Response:
    """
    Update a artifact in ElasticSearch
    """
    try:
        res = payload.save(artifact_id)
        logger.info("artifact updated: %s", res["_id"])
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content={"id": artifact_id},
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@artifact_router.delete("/{artifact_id}", **delete.fastapi_endpoint_config)
def artifact_delete(artifact_id: str) -> JSONResponse | Response:
    """
    Delete a Artifact in ElasticSearch
    """
    try:
        es = es_client()
        res = es.delete(index=es_index, id=artifact_id)

        if res["result"] != "deleted":
            logger.error("Failed to delete Artifact: %s", artifact_id)
            raise Exception(
                f"Failed to delete Artifact. ElasticSearch Response: {res['result']}"
            )

        success_msg = "Artifact successfully deleted: %s", artifact_id

        logger.info(success_msg)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content={"message": success_msg},
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )
