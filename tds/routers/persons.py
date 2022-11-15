"""
tds.router.persons - crud operations for persons and related tables in the DB
"""

import json
from logging import Logger

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import request_rdb

logger = Logger(__file__)
router = APIRouter()


@router.get("")
def get_persons(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a count of persons
    """
    with Session(rdb) as session:
        return (
            session.query(orm.Person).order_by(orm.Person.id.asc()).limit(count).all()
        )


@router.get("/{id}")
def get_person(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific person by ID
    """
    with Session(rdb) as session:
        return session.query(orm.Person).get(id)


@router.post("")
def create_person(payload: schema.Person, rdb: Engine = Depends(request_rdb)):
    """
    Create a person
    """
    with Session(rdb) as session:
        personp = payload.dict()
        del personp["id"]
        person = orm.Person(**personp)
        session.add(person)
        session.commit()
        data_id = person.id
        personp["person_id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/persons/{data_id}",
                "content-type": "application/json",
            },
            content=json.dumps(personp),
        )


@router.patch("/{id}")
def update_person(
    payload: schema.Person, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Update a person by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Person).filter(orm.Person.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Person"


@router.delete("/{id}")
def delete_person(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Delete a person by ID
    """
    with Session(rdb) as session:
        session.query(orm.Person).filter(orm.Person.id == id).delete()
        session.commit()


@router.get("")
def get_associations(count: int = 100, rdb: Engine = Depends(request_rdb)):
    """
    Get a specific number of associations
    """
    with Session(rdb) as session:
        return list(
            session.query(orm.Association)
            .order_by(orm.Association.id.asc())
            .limit(count)
        )


@router.get("/{id}")
def get_association(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific association by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Association).get(id)
        return result


@router.post("")
def create_association(payload: schema.Association, rdb: Engine = Depends(request_rdb)):
    """
    Create a association
    """
    with Session(rdb) as session:
        associationp = payload.dict()
        del associationp["id"]
        association = orm.Association(**associationp)
        session.add(association)
        session.commit()
        data_id = association.id
        associationp["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/associations/{data_id}",
                "content-type": "application/json",
            },
            content=json.dumps(associationp),
        )


@router.patch("/{id}")
def update_association(
    payload: schema.Association, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Update a association by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Association).filter(orm.Association.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated association"


@router.delete("/{id}")
def delete_association(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Delete a association by ID
    """
    with Session(rdb) as session:
        session.query(orm.Association).filter(orm.Association.id == id).delete()
        session.commit()
