"""
CRUD operations for plans and runs
"""
import json
import os
from logging import Logger
from typing import List

import boto3
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
from tds.db import entry_exists, list_by_id, request_rdb
from tds.lib.simulations import adjust_run_params
from tds.operation import create, retrieve, update
from tds.schema.simulation import (
    Run,
    RunDescription,
    SimulationParameters,
    orm_to_params,
)
from tds.settings import settings

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

logger = Logger(__name__)
router = APIRouter()


@router.get("/runs/descriptions", **retrieve.fastapi_endpoint_config)
def list_run_descriptions(
    page_size: int = 100, page: int = 0, rdb: Engine = Depends(request_rdb)
) -> List[RunDescription]:
    """
    Retrieve all simulation run for all plans
    """
    return list_by_id(rdb.connect(), orm.SimulationRun, page_size, page)


@router.get("/runs/{id}/descriptions", **retrieve.fastapi_endpoint_config)
def get_run_description(id: int, rdb: Engine = Depends(request_rdb)) -> RunDescription:
    """
    Retrieve run metadata
    """
    with Session(rdb) as session:
        if entry_exists(rdb.connect(), orm.SimulationRun, id):
            return RunDescription.from_orm(session.query(orm.SimulationRun).get(id))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/runs/descriptions", **create.fastapi_endpoint_config)
def create_run_from_description(
    payload: RunDescription, rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Create a run with no parameters initialized
    """
    with Session(rdb) as session:
        run_payload = payload.dict()
        run = orm.SimulationRun(**run_payload)
        session.add(run)
        session.commit()
        id: int = run.id

    logger.info("new run with %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )


@router.get("/simulation_parameters/{id}", **retrieve.fastapi_endpoint_config)
def get_single_simulation_parameter(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Retrieve simulation parameter
    """
    with Session(rdb) as session:
        if (
            session.query(orm.SimulationParameter)
            .filter(orm.SimulationParameter.id == id)
            .count()
            == 1
        ):
            return session.query(orm.SimulationParameter).get(id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/runs/{id}/parameters", **retrieve.fastapi_endpoint_config)
def get_run_parameters(
    id: int, rdb: Engine = Depends(request_rdb)
) -> SimulationParameters:
    """
    Get run parameters
    """
    with Session(rdb) as session:
        if entry_exists(rdb.connect(), orm.SimulationRun, id):
            parameters: Query[orm.SimulationParameter] = session.query(
                orm.SimulationParameter
            ).filter(orm.SimulationParameter.run_id == id)
            return orm_to_params(list(parameters))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/runs/{id}/parameters", **update.fastapi_endpoint_config)
def update_run_parameters(
    payload: SimulationParameters, id: int, rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Update the parameters for a run
    """
    with Session(rdb) as session:
        adjust_run_params(id, payload, session)
        session.commit()
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
    )


@router.get("/runs/{id}", **retrieve.fastapi_endpoint_config)
def get_run(id: int, rdb: Engine = Depends(request_rdb)) -> Run:
    """
    Retrieve full run
    """
    with Session(rdb) as session:
        if entry_exists(rdb.connect(), orm.SimulationRun, id):
            parameters: Query[orm.SimulationParameter] = session.query(
                orm.SimulationParameter
            ).filter(orm.SimulationParameter.run_id == id)
            return Run.from_orm(
                session.query(orm.SimulationRun).get(id), list(parameters)
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/runs", **create.fastapi_endpoint_config)
def create_run(payload: Run, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Create run with parameters
    """
    with Session(rdb) as session:
        run_payload = payload.dict()
        parameters = run_payload.pop("parameters")
        run = orm.SimulationRun(**run_payload)
        session.add(run)
        session.commit()
        id: int = run.id

        for param in parameters:
            session.add(
                orm.SimulationParameter(
                    run_id=id,
                    name=param["name"],
                    value=param["value"],
                    type=param["type"],
                )
            )
        session.commit()
    logger.info("new run with %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )


@router.get("/runs/{id}/upload-url")
def run_result_upload_url(id: str | int, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to upload to a secure S3 bucket
    without end-user authentication.
    """
    s3_key = os.path.join(settings.S3_RESULT_PATH, str(id), filename)
    put_url = s3.generate_presigned_url(
        ClientMethod="put_object", Params={"Bucket": settings.S3_BUCKET, "Key": s3_key}
    )
    return JSONResponse(
        content={
            "url": put_url,
            "method": "PUT",
        }
    )


@router.get("/runs/{id}/download-url")
def run_result_download_url(id: str | int, filename: str) -> JSONResponse:
    """
    Generates a pre-signed url to allow a user to donwload from a secure S3 bucket
    without the bucket being public or end-user authentication.
    """
    s3_key = os.path.join(settings.S3_RESULT_PATH, str(id), filename)
    get_url = s3.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": settings.S3_BUCKET, "Key": s3_key}
    )
    return JSONResponse(
        content={
            "url": get_url,
            "method": "GET",
        }
    )
