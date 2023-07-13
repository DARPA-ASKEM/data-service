"""
    TDS External Controller.

    Description: Defines the basic rest endpoints for the TDS Module.
"""
from logging import Logger

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from tds.db import entry_exists, request_rdb
from tds.modules.external.model import (
    Publication,
    PublicationPayload,
    Software,
    SoftwarePayload,
)
from tds.operation import create, delete, retrieve, update

external_router = APIRouter()
logger = Logger(__name__)


@external_router.get(
    "/software",
    response_model=list[SoftwarePayload],
    **retrieve.fastapi_endpoint_config,
)
def list_software(
    page_size: int = 100, page: int = 0, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Retrieve list of software from db.
    """
    with Session(rdb) as session:
        software = session.query(Software).all()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(software),
        )


@external_router.post("/software", **create.fastapi_endpoint_config)
def software_post(
    payload: SoftwarePayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Create software and return its ID
    """
    software_payload = payload.dict()

    with Session(rdb) as session:
        software = Software(**software_payload)
        session.add(software)
        session.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            headers={
                "content-type": "application/json",
            },
            content={"id": software.id},
        )


@external_router.get(
    "/software/{software_id}",
    response_model=SoftwarePayload,
    **retrieve.fastapi_endpoint_config,
)
def software_get(software_id: int, rdb: Engine = Depends(request_rdb)) -> JSONResponse:
    """
    Retrieve software record from DB.
    """
    try:
        with Session(rdb) as session:
            software = session.query(Software).filter(Software.id == software_id).all()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                headers={
                    "content-type": "application/json",
                },
                content=jsonable_encoder(software),
            )
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={"message": f"Software with id {software_id} does not exist."},
        )


@external_router.put("/software/{software_id}", **update.fastapi_endpoint_config)
def software_put(
    software_id: int, payload: SoftwarePayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Update software record in DB
    """
    try:
        if entry_exists(rdb.connect(), Software, software_id):
            software_payload = payload.dict()
            software_payload.pop("id")
            with Session(rdb) as session:
                session.query(Software).filter(Software.id == software_id).update(
                    software_payload
                )
                session.commit()

                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    headers={
                        "content-type": "application/json",
                    },
                    content={"id": software_id},
                )
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Software with id of {software_id} does not exist.",
            },
        )


@external_router.delete("/software/{software_id}", **delete.fastapi_endpoint_config)
def software_delete(
    software_id: int, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Delete software record in DB
    """
    try:
        if entry_exists(rdb.connect(), Software, software_id):
            with Session(rdb) as session:
                session.query(Software).filter(Software.id == software_id).delete()
                session.commit()

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                headers={
                    "content-type": "application/json",
                },
                content={"message": f"Software with id {software_id} deleted."},
            )
        raise NoResultFound
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={"message": f"Software with id {software_id} does not exist."},
        )


@external_router.get(
    "/publications",
    response_model=PublicationPayload,
    **retrieve.fastapi_endpoint_config,
)
def publication_list(
    page_size: int = 100, page: int = 0, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Retrieve a publication record from DB.
    """
    with Session(rdb) as session:
        publications = session.query(Publication).all()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(publications),
        )


@external_router.post("/publications", **create.fastapi_endpoint_config)
def publication_post(
    payload: PublicationPayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Create a publication and return its ID
    """
    publication_payload = payload.dict()
    xdd_uri = str(publication_payload["xdd_uri"])
    with Session(rdb) as session:
        publications = (
            session.query(Publication).filter(Publication.xdd_uri == xdd_uri).all()
        )

        if len(publications) < 1:
            publication = Publication(**publication_payload)
            session.add(publication)
            session.commit()

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                headers={
                    "content-type": "application/json",
                },
                content={"id": publication.id},
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Publication with xdd_uri of {xdd_uri} exists",
                "id": publications[0].id,
            },
        )


@external_router.get(
    "/publications/{publication_id}",
    response_model=PublicationPayload,
    **retrieve.fastapi_endpoint_config,
)
def publication_get(
    publication_id: int, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Retrieve a publication record from DB.
    """
    try:
        with Session(rdb) as session:
            publication = session.query(Publication).get(publication_id)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                headers={
                    "content-type": "application/json",
                },
                content=jsonable_encoder(publication),
            )
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Publication with id {publication_id} does not exist."
            },
        )


@external_router.put("/publications/{publication_id}", **create.fastapi_endpoint_config)
def publication_put(
    publication_id: int, payload: PublicationPayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Update a publication and return its ID
    """
    try:
        if entry_exists(rdb.connect(), Publication, publication_id):
            publication_payload = payload.dict()
            publication_payload.pop("id")
            with Session(rdb) as session:
                session.query(Publication).filter(
                    Publication.id == publication_id
                ).update(publication_payload)
                session.commit()

                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    headers={
                        "content-type": "application/json",
                    },
                    content={"id": publication_id},
                )
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Publication with id of {publication_id} does not exist.",
            },
        )


@external_router.delete(
    "/publications/{publication_id}", **delete.fastapi_endpoint_config
)
def publication_delete(
    publication_id: int, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Delete publication record in DB
    """
    try:
        if entry_exists(rdb.connect(), Publication, publication_id):
            with Session(rdb) as session:
                session.query(Publication).filter(
                    Publication.id == publication_id
                ).delete()
                session.commit()

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                headers={
                    "content-type": "application/json",
                },
                content={"message": f"Publication with id {publication_id} deleted."},
            )
        raise NoResultFound
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Publication with id {publication_id} does not exist."
            },
        )
