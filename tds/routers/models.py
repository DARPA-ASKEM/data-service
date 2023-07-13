"""
CRUD operations for models
"""

import json
from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.db import request_rdb
from tds.modules.model.model import ModelFramework, ModelFrameworkPayload
from tds.operation import create, delete, retrieve

logger = Logger(__name__)
router = APIRouter()


@router.post("/frameworks", **create.fastapi_endpoint_config)
def create_framework(
    payload: ModelFrameworkPayload, rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Create framework metadata
    """

    with Session(rdb) as session:
        framework_payload = payload.dict()
        framework = ModelFramework(**framework_payload)
        session.add(framework)
        session.commit()
        name: str = framework.name
    logger.info("new framework with %i", name)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"name": name}),
    )


@router.get("/frameworks/{name}", **retrieve.fastapi_endpoint_config)
def get_framework(name: str, rdb: Engine = Depends(request_rdb)) -> ModelFramework:
    """
    Retrieve framework metadata
    """
    with Session(rdb) as session:
        if (
            session.query(ModelFramework).filter(ModelFramework.name == name).count()
            == 1
        ):
            return ModelFramework.from_orm(session.query(ModelFramework).get(name))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/frameworks/{name}", **delete.fastapi_endpoint_config)
def delete_framework(name: str, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Delete framework metadata
    """
    with Session(rdb) as session:
        if (
            session.query(ModelFramework).filter(ModelFramework.name == name).count()
            == 1
        ):
            framework = session.query(ModelFramework).get(name)
            session.delete(framework)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
