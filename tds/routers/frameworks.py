"""
router.framework - very basic crud operations for frameworks
"""

from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db import request_rdb
from tds.operation import create, delete, retrieve
from tds.schema.framework import ModelFramework

logger = Logger(__name__)
router = APIRouter()


@router.get("/{name}", **retrieve.fastapi_endpoint_config)
def get_framework(name: str, rdb: Engine = Depends(request_rdb)) -> ModelFramework:
    """
    Retrieve framework metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.ModelFramework)
            .filter(orm.ModelFramework.name == name)
            .count()
            == 1
        ):
            return ModelFramework.from_orm(session.query(orm.ModelFramework).get(name))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("", **create.fastapi_endpoint_config)
def create_framework(
    payload: ModelFramework, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Create framework metadata
    """

    with Session(rdb) as session:
        framework_payload = payload.dict()
        framework = orm.ModelFramework(**framework_payload)
        session.add(framework)
        session.commit()
    logger.info("new framework with %i", framework_payload.get("name"))
    return framework_payload.get("name")


@router.delete("/{name}", **delete.fastapi_endpoint_config)
def delete_framework(name: str, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Delete framework metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.ModelFramework)
            .filter(orm.ModelFramework.name == name)
            .count()
            == 1
        ):
            framework = session.query(orm.ModelFramework).get(name)
            session.delete(framework)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
