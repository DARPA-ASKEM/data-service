"""
    TDS Code Controller.

    Description: Defines the basic rest endpoints for the TDS Module.
"""
from logging import Logger

from elasticsearch import NotFoundError
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tds.db import es_client
from tds.lib.s3 import get_presigned_url
from tds.modules.code.model import Code
from tds.modules.code.response import CodeResponse, code_response
from tds.operation import create, delete, retrieve, update
from tds.settings import settings

code_router = APIRouter()
logger = Logger(__name__)
es_index = Code.index


@code_router.get(
    "", response_model=list[CodeResponse], **retrieve.fastapi_endpoint_config
)
def list_codes(page_size: int = 100, page: int = 0) -> JSONResponse:
    """
    Retrieve the list of codes from ES.
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
        content=jsonable_encoder(code_response(res["hits"]["hits"])),
    )


@code_router.post("", **create.fastapi_endpoint_config)
def code_post(payload: Code) -> JSONResponse:
    """
    Create code and return its ID
    """
    res = payload.save()
    logger.info("New code created: %s", res["_id"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@code_router.get(
    "/{code_id}", response_model=CodeResponse, **retrieve.fastapi_endpoint_config
)
def code_get(code_id: str) -> JSONResponse:
    """
    Retrieve a code from ElasticSearch
    """
    try:
        es = es_client()
        res = es.get(index=es_index, id=code_id)
        logger.info("Code retrieved: %s", code_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(CodeResponse(**res["_source"])),
        )
    except NotFoundError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={"message": f"Code segment with id {code_id} was not found."},
        )


@code_router.put("/{code_id}", **update.fastapi_endpoint_config)
def code_put(code_id: str, payload: Code) -> JSONResponse:
    """
    Update a code in ElasticSearch
    """
    try:
        res = payload.save()
        logger.info("code updated: %s", res["_id"])
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content={"id": code_id},
        )
    except NotFoundError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={"message": f"Code segment with id {code_id} was not found."},
        )


@code_router.delete("/{code_id}", **delete.fastapi_endpoint_config)
def code_delete(code_id: str) -> JSONResponse:
    """
    Delete a Code in ElasticSearch
    """
    try:
        es = es_client()
        res = es.delete(index=es_index, id=code_id)

        if res["result"] != "deleted":
            logger.error("Failed to delete Code: %s", code_id)
            raise Exception(
                f"Failed to delete Code. ElasticSearch Response: {res['result']}"
            )

        success_msg = "Code successfully deleted: %s", code_id

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
            content={"message": f"Code segment with id {code_id} was not found."},
        )


@code_router.get("/{code_id}/upload-url")
def dataset_upload_url(code_id: str, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to upload to a secure S3 bucket
    without end-user authentication.
    """
    put_url = get_presigned_url(
        entity_id=code_id,
        file_name=filename,
        method="put_object",
        path=settings.S3_CODE_PATH,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "url": put_url,
            "method": "PUT",
        },
    )


@code_router.get("/{code_id}/download-url")
def dataset_download_url(code_id: str, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to donwload from a secure S3 bucket
    without the bucket being public or end-user authentication.
    """
    get_url = get_presigned_url(
        entity_id=code_id,
        file_name=filename,
        method="get_object",
        path=settings.S3_CODE_PATH,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "url": get_url,
            "method": "GET",
        },
    )
