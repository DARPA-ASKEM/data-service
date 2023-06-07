"""
    TDS Simulation Controller.

    Description: Defines the basic rest endpoints for the TDS Module.
"""
from logging import Logger

from elasticsearch import NotFoundError
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tds.db import es_client
from tds.lib.s3 import get_presigned_url
from tds.modules.simulation.model import Simulation
from tds.modules.simulation.response import SimulationResponse, simulation_response
from tds.operation import create, delete, retrieve, update

simulation_router = APIRouter()
logger = Logger(__name__)
es_index = Simulation.index


@simulation_router.get(
    "", response_model=list[SimulationResponse], **retrieve.fastapi_endpoint_config
)
def list_simulations(page_size: int = 100, page: int = 0) -> JSONResponse:
    """
    Retrieve the list of simulations from ES.
    """
    es = es_client()
    list_body = {"size": page_size, "from_": page}

    res = es.search(index=es_index, **list_body)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=jsonable_encoder(simulation_response(res["hits"]["hits"])),
    )


@simulation_router.post("", **create.fastapi_endpoint_config)
def simulation_post(payload: Simulation) -> JSONResponse:
    """
    Create simulation and return its ID
    """
    res = payload.save()
    logger.info("New simulation created: %s", res["_id"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@simulation_router.get(
    "/{simulation_id}",
    response_model=SimulationResponse,
    **retrieve.fastapi_endpoint_config,
)
def simulation_get(simulation_id: str) -> JSONResponse | Response:
    """
    Retrieve a simulation from ElasticSearch
    """
    try:
        es = es_client()
        res = es.get(index=es_index, id=simulation_id)
        logger.info("Simulation retrieved: %s", simulation_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(SimulationResponse(**res["_source"])),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@simulation_router.put("/{simulation_id}", **update.fastapi_endpoint_config)
def simulation_put(simulation_id: str, payload: Simulation) -> JSONResponse | Response:
    """
    Update a simulation in ElasticSearch
    """
    try:
        res = payload.save()
        logger.info("simulation updated: %s", res["_id"])
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content={"id": simulation_id},
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@simulation_router.delete("/{simulation_id}", **delete.fastapi_endpoint_config)
def simulation_delete(simulation_id: str) -> JSONResponse | Response:
    """
    Delete a Simulation in ElasticSearch
    """
    try:
        es = es_client()
        res = es.delete(index=es_index, id=simulation_id)

        if res["result"] != "deleted":
            logger.error("Failed to delete Simulation: %s", simulation_id)
            raise Exception(
                f"Failed to delete Simulation. ElasticSearch Response: {res['result']}"
            )

        success_msg = "Simulation successfully deleted: %s", simulation_id

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


@simulation_router.get("/{simulation_id}/upload-url")
def run_result_upload_url(simulation_id: str, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to upload to a secure S3 bucket
    without end-user authentication.
    """
    put_url = get_presigned_url(
        entity_id=simulation_id, file_name=filename, method="put_object"
    )
    return JSONResponse(
        content={
            "url": put_url,
            "method": "PUT",
        }
    )


@simulation_router.get("/{simulation_id}/download-url")
def run_result_download_url(simulation_id: str, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to donwload from a secure S3 bucket
    without the bucket being public or end-user authentication.
    """
    get_url = get_presigned_url(
        entity_id=simulation_id, file_name=filename, method="get_object"
    )
    return JSONResponse(
        content={
            "url": get_url,
            "method": "GET",
        }
    )
