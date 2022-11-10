"""
router.software - very basic crud operations for software
"""

from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db import request_rdb
from tds.operation import create, delete, retrieve
from tds.schema.software import Software

logger = Logger(__name__)
router = APIRouter()


@router.get("/{id}", **retrieve.fastapi_endpoint_config)
def get_software(id: int, rdb: Engine = Depends(request_rdb)) -> Software:
    """
    Retrieve software metadata
    """
    with Session(rdb) as session:
        if session.query(orm.Software).filter(orm.Software.id == id).count() == 1:
            return Software.from_orm(session.query(orm.Software).get(id))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("", **create.fastapi_endpoint_config)
def create_software(payload: Software, rdb: Engine = Depends(request_rdb)) -> int:
    """
    Create software metadata
    """
    with Session(rdb) as session:
        software_payload = payload.dict()
        software = orm.Software(**software_payload)
        session.add(software)
        session.commit()
        id: int = software.id
    logger.info("new software with %i", id)
    return id


@router.delete("/{id}", **delete.fastapi_endpoint_config)
def delete_software(id: int, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Delete software metadata
    """
    with Session(rdb) as session:
        if session.query(orm.Software).filter(orm.Software.id == id).count() == 1:
            software = session.query(orm.Software).get(id)
            session.delete(software)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
