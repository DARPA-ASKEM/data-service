"""
TDS Dataset
"""
import os.path
from logging import Logger
from typing import List

import boto3
from elasticsearch import NotFoundError
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from tds.db.elasticsearch import es_client
from tds.modules.dataset.model import Dataset
from tds.operation import create, delete, retrieve, update
from tds.settings import settings

dataset_router = APIRouter()
logger = Logger(__name__)
es_index = Dataset.index

if settings.STORAGE_HOST:
    s3 = boto3.client(
        "s3",
        endpoint_url=settings.STORAGE_HOST,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=None,
        config=boto3.session.Config(signature_version="s3v4"),
        verify=False,
    )
else:
    s3 = boto3.client("s3")
es = es_client()


@dataset_router.get("", **retrieve.fastapi_endpoint_config)
def list_datasets(page_size: int = 100, page: int = 0) -> List[Dataset]:
    """
    Retrieve the list of models from ES.
    """
    list_body = {
        "size": page_size,
    }
    if page != 0:
        list_body["from"] = page
    res = es.search(index=es_index, **list_body)
    return [Dataset(**hit["_source"]) for hit in res["hits"]["hits"]]


@dataset_router.post("", **create.fastapi_endpoint_config)
def create_dataset(payload: Dataset) -> JSONResponse:
    """
    Create model and return its ID
    """
    res = payload.create()
    logger.info("New dataset created: %s", id)
    return JSONResponse(
        status_code=201,
        content={"id": res["_id"]},
    )


@dataset_router.get("/{dataset_id}", **retrieve.fastapi_endpoint_config)
def dataset_get(dataset_id: str | int) -> Dataset:
    """
    Returns a full representation of a Dataset
    """
    try:
        res = es.get(index=es_index, id=dataset_id)
        logger.info("dataset retrieved: %s", dataset_id)

        return Dataset(**res["_source"])
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc


@dataset_router.put("/{dataset_id}", **update.fastapi_endpoint_config)
def dataset_put(dataset_id: str | int, payload: Dataset) -> JSONResponse:
    """
    Update dataset with full payload
    """
    if payload.id != dataset_id:
        raise HTTPException(
            status_code=422, detail="ID in request URL and in payload must match."
        )
    res = payload.save()
    logger.info("dataset updated: %s", dataset_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"id": res["_id"]},
    )


@dataset_router.patch("/{dataset_id}", **update.fastapi_endpoint_config)
def dataset_patch(dataset_id: str | int, payload: Dataset) -> Dataset:
    """
    Update a dataset with partial upload
    """

    update_data = payload.dict(exclude_unset=True)
    orig_dataset = dataset_get(dataset_id)

    if update_data.get("id", dataset_id) != dataset_id or orig_dataset.id != dataset_id:
        raise HTTPException(
            status_code=422,
            detail="ID in request URL, the payload, and the stored data must match.",
        )

    dataset = orig_dataset.copy(update=payload)
    dataset.save()
    return dataset


# @dataset_router.post("/deprecate/{dataset_id}")
# def deprecate_dataset(dataset_id: str | int, payload: Dataset) -> Response:
#     """
#     Toggle a dataset's deprecated status by ID
#     """
#     pass


@dataset_router.delete("/{dataset_id}", **delete.fastapi_endpoint_config)
def dataset_delete(dataset_id: str | int) -> JSONResponse:
    """
    Removes a dataset document from elasticsearch
    """
    try:
        res = es.delete(index=es_index, id=dataset_id)

        if res["result"] != "deleted":
            logger.error("Failed to delete dataset: %s", dataset_id)
            raise Exception(
                f"Failed to delete dataset. ElasticSearch Response: {res['result']}"
            )

        logger.info("dataset successfully deleted: %s", dataset_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={})
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc


@dataset_router.get("/{dataset_id}/upload-url")
def dataset_upload_url(dataset_id: str | int, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to upload to a secure S3 bucket
    without end-user authentication.
    """
    s3_key = os.path.join(settings.S3_DATASET_PATH, str(dataset_id), filename)
    put_url = s3.generate_presigned_url(
        ClientMethod="put_object", Params={"Bucket": settings.S3_BUCKET, "Key": s3_key}
    )
    return JSONResponse(
        content={
            "url": put_url,
            "method": "PUT",
        }
    )


@dataset_router.get("/{dataset_id}/download-url")
def dataset_download_url(dataset_id: str | int, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to donwload from a secure S3 bucket
    without the bucket being public or end-user authentication.
    """
    s3_key = os.path.join(settings.S3_DATASET_PATH, str(dataset_id), filename)
    get_url = s3.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": settings.S3_BUCKET, "Key": s3_key}
    )
    return JSONResponse(
        content={
            "url": get_url,
            "method": "GET",
        }
    )
