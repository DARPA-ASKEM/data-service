"""
TDS  Notebook Session Controller.
"""
from logging import Logger

from elasticsearch import NotFoundError
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tds.db import es_client
from tds.modules.notebook_session.model import NotebookSession
from tds.modules.notebook_session.response import (
    NotebookSessionResponse,
    notebook_session_response,
)
from tds.operation import create, delete, retrieve, update

notebook_session_router = APIRouter()
logger = Logger(__name__)
es_index = NotebookSession.index


@notebook_session_router.get(
    "", response_model=list[NotebookSessionResponse], **retrieve.fastapi_endpoint_config
)
def list_notebook_sessions(page_size: int = 100, page: int = 0) -> JSONResponse:
    """
    Retrieve the list of notebook_sessions from ES.
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
        content=jsonable_encoder(notebook_session_response(res["hits"]["hits"])),
    )


@notebook_session_router.post("", **create.fastapi_endpoint_config)
def notebook_session_post(payload: NotebookSession) -> JSONResponse:
    """
    Create notebook_session and return its ID
    """
    print(payload)
    res = payload.save()
    logger.info("New notebook_session created: %s", res["_id"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@notebook_session_router.get(
    "/{notebook_session_id}",
    response_model=NotebookSessionResponse,
    **retrieve.fastapi_endpoint_config,
)
def notebook_session_get(notebook_session_id: str) -> JSONResponse:
    """
    Retrieve a notebook_session from ElasticSearch
    """
    try:
        es = es_client()
        res = es.get(index=es_index, id=notebook_session_id)
        logger.info("NotebookSession retrieved: %s", notebook_session_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(NotebookSessionResponse(**res["_source"])),
        )
    except NotFoundError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Notebook session with id "
                f"{notebook_session_id} does not exist.",
            },
        )


@notebook_session_router.put("/{notebook_session_id}", **update.fastapi_endpoint_config)
def notebook_session_put(
    notebook_session_id: str, payload: NotebookSession
) -> JSONResponse:
    """
    Update a notebook_session in ElasticSearch
    """
    try:
        res = payload.save()
        logger.info("notebook_session updated: %s", res["_id"])
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content={"id": notebook_session_id},
        )
    except NotFoundError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Notebook session with id "
                f"{notebook_session_id} does not exist.",
            },
        )


@notebook_session_router.delete(
    "/{notebook_session_id}", **delete.fastapi_endpoint_config
)
def notebook_session_delete(notebook_session_id: str) -> JSONResponse:
    """
    Delete a NotebookSession in ElasticSearch
    """
    try:
        es = es_client()
        res = es.delete(index=es_index, id=notebook_session_id)

        if res["result"] != "deleted":
            logger.error("Failed to delete NotebookSession: %s", notebook_session_id)
            raise Exception(
                f"Failed to delete NotebookSession. ElasticSearch Response: "
                f"{res['result']}"
            )

        success_msg = f"NotebookSession successfully deleted: {notebook_session_id}"

        logger.info(success_msg)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content={"message": success_msg},
        )
    except NotFoundError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Notebook session with id "
                f"{notebook_session_id} does not exist.",
            },
        )
