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


@router.get("/{id}", **retrieve.fastapi_endpoint_config)
def get_framework(id: int, rdb: Engine = Depends(request_rdb)) -> ModelFramework:
    """
    Retrieve framework metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.ModelFramework)
            .filter(orm.ModelFramework.id == id)
            .count()
            == 1
        ):
            return ModelFramework.from_orm(session.query(orm.ModelFramework).get(id))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("", **create.fastapi_endpoint_config)
def create_framework(
    payload: ModelFramework, rdb: Engine = Depends(request_rdb)
) -> int:
    """
    Create framework metadata
    """
    with Session(rdb) as session:
        framework_payload = payload.dict()
        print(framework_payload)
        framework = orm.ModelFramework(**framework_payload)
        session.add(framework)
        session.commit()
    logger.info("new framework with %i", framework.name)
    return framework.name


@router.delete("/{id}", **delete.fastapi_endpoint_config)
def delete_framework(id: int, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Delete framework metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.ModelFramework)
            .filter(orm.ModelFramework.id == id)
            .count()
            == 1
        ):
            framework = session.query(orm.ModelFramework).get(id)
            session.delete(framework)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
