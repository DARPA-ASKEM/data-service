"""
TDS Framework Controller.
"""
from logging import Logger

from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from tds.db import request_rdb
from tds.modules.framework.response import ModelFrameworkResponse
from tds.modules.model.model import ModelFramework, ModelFrameworkPayload
from tds.operation import create, delete, retrieve, update

framework_router = APIRouter()
logger = Logger(__name__)


@framework_router.get(
    "", response_model=list[ModelFrameworkResponse], **retrieve.fastapi_endpoint_config
)
def list_frameworks(
    page_size: int = 100, page: int = 0, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Retrieve the list of frameworks.
    """
    with Session(rdb) as session:
        frameworks = session.query(ModelFramework).all()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(frameworks),
        )


@framework_router.post("", **create.fastapi_endpoint_config)
def framework_post(
    payload: ModelFrameworkPayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Create framework and return its ID
    """
    framework_payload = payload.dict()
    name = framework_payload["name"]
    try:
        with Session(rdb) as session:
            model_framework = ModelFramework(**framework_payload)
            session.add(model_framework)
            session.commit()

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                headers={
                    "content-type": "application/json",
                },
                content={"name": name},
            )
    except IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            headers={
                "content-type": "application/json",
            },
            content={"message": f"A framework with the name {name} already exists."},
        )


@framework_router.get(
    "/{framework_name}",
    response_model=ModelFrameworkResponse,
    **retrieve.fastapi_endpoint_config,
)
def framework_get(
    framework_name: str, rdb: Engine = Depends(request_rdb)
) -> JSONResponse | Response:
    """
    Retrieve a framework from ElasticSearch
    """
    try:
        with Session(rdb) as session:
            framework = (
                session.query(ModelFramework)
                .filter(ModelFramework.name == framework_name)
                .all()
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                headers={
                    "content-type": "application/json",
                },
                content=jsonable_encoder(framework),
            )
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Model Framework with id {framework_name} does not exist."
            },
        )


@framework_router.put("/{framework_name}", **update.fastapi_endpoint_config)
def framework_put(
    framework_name: str,
    payload: ModelFrameworkPayload,
    rdb: Engine = Depends(request_rdb),
) -> JSONResponse | Response:
    """
    Update a framework in ElasticSearch
    """
    try:
        framework_payload = payload.dict()
        with Session(rdb) as session:
            if (
                session.query(ModelFramework)
                .filter(ModelFramework.name == framework_name)
                .count()
                > 0
            ):
                session.query(ModelFramework).filter(
                    ModelFramework.name == framework_name
                ).update(framework_payload)
                session.commit()
                logger.info("framework updated: %s", framework_name)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    headers={
                        "content-type": "application/json",
                    },
                    content={"name": framework_name},
                )
            raise NoResultFound
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Framework with name {framework_name} does not exist."
            },
        )


@framework_router.delete("/{framework_name}", **delete.fastapi_endpoint_config)
def framework_delete(
    framework_name: str, rdb: Engine = Depends(request_rdb)
) -> JSONResponse | Response:
    """
    Delete a Framework in ElasticSearch
    """
    try:
        with Session(rdb) as session:
            if (
                session.query(ModelFramework)
                .filter(ModelFramework.name == framework_name)
                .count()
                > 0
            ):
                session.query(ModelFramework).filter(
                    ModelFramework.name == framework_name
                ).delete()
                session.commit()
                success_msg = f"Framework successfully deleted: {framework_name}"
                logger.info(success_msg)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    headers={
                        "content-type": "application/json",
                    },
                    content={"message": success_msg},
                )
            raise NoResultFound
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Framework with name {framework_name} does not exist."
            },
        )
