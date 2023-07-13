"""
    TDS Person Controller.
"""
from logging import Logger

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from tds.db import entry_exists, list_by_id, request_rdb
from tds.modules.person.model import (
    Association,
    AssociationPayload,
    Person,
    PersonPayload,
)
from tds.modules.person.response import PersonResponse
from tds.operation import create, delete, retrieve, update

person_router = APIRouter()
logger = Logger(__name__)


@person_router.get(
    "", response_model=list[PersonResponse], **retrieve.fastapi_endpoint_config
)
def list_persons(
    page_size: int = 100, page: int = 0, rdb: Engine = Depends(request_rdb)
):
    """
    Page over persons
    """
    people = list_by_id(rdb.connect(), Person, page_size, page)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=jsonable_encoder(people),
    )


@person_router.post("", **create.fastapi_endpoint_config)
def person_post(
    payload: PersonPayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Create person and return its ID
    """
    try:
        with Session(rdb) as session:
            record = Person(**payload.dict())
            session.add(record)
            session.commit()

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                headers={
                    "content-type": "application/json",
                },
                content={"id": record.id},
            )
    except SQLAlchemyError as error:
        logger.error(error)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers={
                "content-type": "application/json",
            },
            content={"message": f"Person was not created."},
        )


@person_router.get(
    "/{person_id}", response_model=PersonResponse, **retrieve.fastapi_endpoint_config
)
def person_get(person_id: int, rdb: Engine = Depends(request_rdb)) -> JSONResponse:
    """
    Retrieve a person from postgres.
    """
    try:
        with Session(rdb) as session:
            person = session.query(Person).get(person_id)
            print(person)

        logger.info("Person retrieved: %s", person_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(person),
        )
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={"message": f"The person with id {person_id} does not exist."},
        )


@person_router.put("/{person_id}", **update.fastapi_endpoint_config)
def person_put(
    person_id: int, payload: PersonPayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Update a person object.
    """
    try:
        if entry_exists(rdb.connect(), Person, person_id):
            with Session(rdb) as session:
                project_payload = payload.dict()

                session.query(Person).filter(Person.id == person_id).update(
                    project_payload
                )
                session.commit()

            logger.info("new project created: %i", person_id)
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                headers={"content-type": "application/json"},
                content={"id": person_id},
            )
    except NoResultFound as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Person with id {person_id} does not exist. {error.code}"
            },
        )


@person_router.delete("/{person_id}", **delete.fastapi_endpoint_config)
def person_delete(person_id: int, rdb: Engine = Depends(request_rdb)) -> JSONResponse:
    """
    Delete a Person
    """
    try:
        if entry_exists(rdb.connect(), Person, person_id):
            with Session(rdb) as session:
                person = session.query(Person).filter(Person.id == person_id).first()
                session.delete(person)
                session.commit()

            logger.info("Person deleted: %i", person_id)
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                headers={"content-type": "application/json"},
                content={"message": f"Person ({person_id}) deleted."},
            )
        raise NoResultFound
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={"message": f"Person with id {person_id} does not exist."},
        )


@person_router.get(
    "/{person_id}/associations",
    response_model=PersonResponse,
    **retrieve.fastapi_endpoint_config,
)
def person_associations(
    person_id: int, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Retrieve a person's associations.
    """
    try:
        if entry_exists(rdb.connect(), Person, person_id):
            with Session(rdb) as session:
                person = session.query(Person).get(person_id)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    headers={
                        "content-type": "application/json",
                    },
                    content=jsonable_encoder(person.associations),
                )
        raise NoResultFound
    except NoResultFound as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Person with id {person_id} does not exist. {error.code}"
            },
        )


@person_router.post("/{person_id}/associations", **create.fastapi_endpoint_config)
def create_association(
    person_id: int, payload: AssociationPayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Create a person -> association record.
    """
    try:
        if entry_exists(rdb.connect(), Person, person_id):
            with Session(rdb) as session:
                person = session.query(Person).get(person_id)
                association = Association(**payload.dict())
                person.associations.append(association)
                session.commit()
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    headers={
                        "content-type": "application/json",
                    },
                    content={"id": association.id},
                )
        raise NoResultFound
    except NoResultFound as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Person with id {person_id} does not exist. {error.code}"
            },
        )


@person_router.delete(
    "/{person_id}/associations/{association_id}", **delete.fastapi_endpoint_config
)
def delete_association(
    person_id: int, association_id: int, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Delete a person -> association record.
    """
    try:
        print(f"Deleting Record...Person:{person_id} -> Association:{association_id}")
        if entry_exists(rdb.connect(), Person, person_id) and entry_exists(
            rdb.connect(), Association, association_id
        ):
            with Session(rdb) as session:
                person = session.query(Person).get(person_id)
                association = session.query(Association).get(association_id)
                print(association)
                print(association.person)
                person.associations.remove(association)
                session.add(person)
                session.commit()
                # session.delete(association)
                # session.commit()
                return JSONResponse(
                    status_code=status.HTTP_202_ACCEPTED,
                    headers={
                        "content-type": "application/json",
                    },
                    content={"message": f"Association {association_id} deleted."},
                )
        raise NoResultFound
    except NoResultFound as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Person with id {person_id} does not have "
                f"an association with id {association_id}. "
                f"{error.code}"
            },
        )


@person_router.get("/{person_id}/associations/{association_id}")
def get_association(
    person_id: int, association_id: int, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Get a specific association by ID
    """
    try:
        if entry_exists(rdb.connect(), Person, person_id) and entry_exists(
            rdb.connect(), Association, association_id
        ):
            with Session(rdb) as session:
                association = session.query(Association).get(association_id)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    headers={
                        "content-type": "application/json",
                    },
                    content=jsonable_encoder(association),
                )
        raise NoResultFound
    except NoResultFound as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={
                "message": f"Person with id {person_id} does not have "
                f"an association with id {association_id}. "
                f"{error.code}"
            },
        )
