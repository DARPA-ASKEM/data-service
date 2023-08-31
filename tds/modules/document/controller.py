"""
    TDS Document Controller.

    Description: Defines the basic rest endpoints for the TDS Module.
"""
from logging import Logger

from elasticsearch import NotFoundError
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tds.db import es_client
from tds.lib.s3 import get_presigned_url
from tds.modules.document.model import Document
from tds.modules.document.response import DocumentResponse, document_response
from tds.operation import create, delete, retrieve, update
from tds.settings import settings

document_router = APIRouter()
logger = Logger(__name__)
es_index = Document.index


@document_router.get(
    "", response_model=list[DocumentResponse], **retrieve.fastapi_endpoint_config
)
def list_documents(page_size: int = 100, page: int = 0) -> JSONResponse:
    """
    Retrieve the list of documents from ES.
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
        content=jsonable_encoder(document_response(res["hits"]["hits"])),
    )


@document_router.post("", **create.fastapi_endpoint_config)
def document_post(payload: Document) -> JSONResponse:
    """
    Create document and return its ID
    """
    res = payload.save()
    logger.info("New document created: %s", res["_id"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@document_router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    **retrieve.fastapi_endpoint_config,
)
def document_get(document_id: str) -> JSONResponse | Response:
    """
    Retrieve a document from ElasticSearch
    """
    try:
        es = es_client()
        res = es.get(index=es_index, id=document_id)
        logger.info("Document retrieved: %s", document_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(DocumentResponse(**res["_source"])),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@document_router.put("/{document_id}", **update.fastapi_endpoint_config)
def document_put(document_id: str, payload: Document) -> JSONResponse | Response:
    """
    Update a document in ElasticSearch
    """
    try:
        payload.id = document_id
        res = payload.save()
        logger.info("document updated: %s", res["_id"])
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content={"id": document_id},
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@document_router.delete("/{document_id}", **delete.fastapi_endpoint_config)
def document_delete(document_id: str) -> JSONResponse | Response:
    """
    Delete a Document in ElasticSearch
    """
    try:
        es = es_client()
        res = es.delete(index=es_index, id=document_id)

        if res["result"] != "deleted":
            logger.error("Failed to delete Document: %s", document_id)
            raise Exception(
                f"Failed to delete Document. ElasticSearch Response: {res['result']}"
            )

        success_msg = "Document successfully deleted: %s", document_id

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


@document_router.get("/{document_id}/upload-url")
def document_upload_url(document_id: str, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to upload to a secure S3 bucket
    without end-user authentication.
    """
    put_url = get_presigned_url(
        entity_id=document_id,
        file_name=filename,
        method="put_object",
        path=settings.S3_DOCUMENT_PATH,
    )
    return JSONResponse(
        content={
            "url": put_url,
            "method": "PUT",
        }
    )


@document_router.get("/{document_id}/download-url")
def document_download_url(document_id: str, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to donwload from a secure S3 bucket
    without the bucket being public or end-user authentication.
    """
    get_url = get_presigned_url(
        entity_id=document_id,
        file_name=filename,
        method="get_object",
        path=settings.S3_DOCUMENT_PATH,
    )
    return JSONResponse(
        content={
            "url": get_url,
            "method": "GET",
        }
    )
