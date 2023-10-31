"""
    TDS equation Controller.

    Description: Defines the basic rest endpoints for the TDS Module.
"""
from logging import Logger

from elasticsearch import NotFoundError
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tds.db import es_client
from tds.lib.s3 import get_presigned_url
from tds.modules.equation.model import equation
from tds.modules.equation.response import equation_response, equationResponse
from tds.operation import create, delete, retrieve, update
from tds.settings import settings

equation_router = APIRouter()
logger = Logger(__name__)
es_index = equation.index


@equation_router.get(
    "", response_model=list[equationResponse], **retrieve.fastapi_endpoint_config
)
def list_equations(page_size: int = 100, page: int = 0) -> JSONResponse:
    """
    Retrieve the list of equations from ES.
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
        content=jsonable_encoder(equation_response(res["hits"]["hits"])),
    )


@equation_router.post("", **create.fastapi_endpoint_config)
def equation_post(payload: equation) -> JSONResponse:
    """
    Create equation and return its ID
    """
    res = payload.save()
    logger.info("New equation created: %s", res["_id"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@equation_router.get(
    "/{equation_id}",
    response_model=equationResponse,
    **retrieve.fastapi_endpoint_config,
)
def equation_get(equation_id: str) -> JSONResponse | Response:
    """
    Retrieve a equation from ElasticSearch
    """
    try:
        es = es_client()
        res = es.get(index=es_index, id=equation_id)
        logger.info("equation retrieved: %s", equation_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(equationResponse(**res["_source"])),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@equation_router.put("/{equation_id}", **update.fastapi_endpoint_config)
def equation_put(equation_id: str, payload: equation) -> JSONResponse | Response:
    """
    Update a equation in ElasticSearch
    """
    try:
        payload.id = equation_id
        res = payload.save()
        logger.info("equation updated: %s", res["_id"])
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content={"id": equation_id},
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@equation_router.delete("/{equation_id}", **delete.fastapi_endpoint_config)
def equation_delete(equation_id: str) -> JSONResponse | Response:
    """
    Delete a equation in ElasticSearch
    """
    try:
        es = es_client()
        res = es.delete(index=es_index, id=equation_id)

        if res["result"] != "deleted":
            logger.error("Failed to delete equation: %s", equation_id)
            raise Exception(
                f"Failed to delete equation. ElasticSearch Response: {res['result']}"
            )

        success_msg = "equation successfully deleted: %s", equation_id

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


@equation_router.get("/{equation_id}/upload-url")
def equation_upload_url(equation_id: str, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to upload to a secure S3 bucket
    without end-user authentication.
    """
    put_url = get_presigned_url(
        entity_id=equation_id,
        file_name=filename,
        method="put_object",
        path=settings.S3_equation_PATH,
    )
    return JSONResponse(
        content={
            "url": put_url,
            "method": "PUT",
        }
    )


@equation_router.get("/{equation_id}/download-url")
def equation_download_url(equation_id: str, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to download from a secure S3 bucket
    without the bucket being public or end-user authentication.
    """
    get_url = get_presigned_url(
        entity_id=equation_id,
        file_name=filename,
        method="get_object",
        path=settings.S3_equation_PATH,
    )
    return JSONResponse(
        content={
            "url": get_url,
            "method": "GET",
        }
    )


# May need to enable discrete asset endpoints in the future, uncomment below:
# @equation_router.get("/{equation_id}/upload-url/asset")
# def asset_upload_url(equation_id: str, filename: str) -> JSONResponse:
#     """
#     Generates a pre-signed url to allow a user to upload to a secure S3 bucket
#     without end-user authentication.
#     """
#     put_url = get_presigned_url(
#         entity_id=equation_id,
#         file_name=filename,
#         method="put_object",
#         path=settings.S3_ASSET_PATH,
#     )
#     return JSONResponse(
#         content={
#             "url": put_url,
#             "method": "PUT",
#         }
#     )

# @equation_router.get("/{equation_id}/download-url/asset")
# def asset_download_url(equation_id: str, filename: str) -> JSONResponse:
#     """
#     Generates a pre-signed url to allow a user to download from a secure S3 bucket
#     without the bucket being public or end-user authentication.
#     """
#     get_url = get_presigned_url(
#         entity_id=equation_id,
#         file_name=filename,
#         method="get_object",
#         path=settings.S3_ASSET_PATH,
#     )
#     return JSONResponse(
#         content={
#             "url": get_url,
#             "method": "GET",
#         }
#     )
