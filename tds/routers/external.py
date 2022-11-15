"""
Basic crud operations for external resources
"""

import json
from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db import entry_exists, request_rdb
from tds.operation import create, delete, retrieve
from tds.schema.resource import Publication, Software

logger = Logger(__name__)
router = APIRouter()


@router.get("/software/{id}", **retrieve.fastapi_endpoint_config)
def get_software(id: int, rdb: Engine = Depends(request_rdb)) -> Software:
    """
    Retrieve software metadata
    """
    with Session(rdb) as session:
        if session.query(orm.Software).filter(orm.Software.id == id).count() == 1:
            return Software.from_orm(session.query(orm.Software).get(id))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/software", **create.fastapi_endpoint_config)
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


@router.delete("/software/{id}", **delete.fastapi_endpoint_config)
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


@router.get("/publications")
def get_publications(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a count of persons
    """
    with Session(rdb) as session:
        return (
            session.query(orm.Publication)
            .order_by(orm.Publication.id.asc())
            .limit(count)
            .all()
        )


@router.get("/publications/{id}", **retrieve.fastapi_endpoint_config)
def get_publication(id: int, rdb: Engine = Depends(request_rdb)) -> Publication:
    """
    Retrieve model
    """
    if entry_exists(rdb.connect(), orm.Publication, id):
        with Session(rdb) as session:
            publication = session.query(orm.Publication).get(id)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Publication.from_orm(publication)


@router.post("/publications", **create.fastapi_endpoint_config)
def create_publication(
    payload: Publication, rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Create publication and return its ID
    """
    with Session(rdb) as session:
        publication_payload = payload.dict()
        # pylint: disable-next=unused-variable
        publication = orm.Publication(**publication_payload)
        session.add(publication)
        session.commit()
        id: int = publication.id

    logger.info("new model created: %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "location": f"/api/publication/{id}",
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )
