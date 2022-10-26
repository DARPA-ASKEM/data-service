"""
router.datasets - crud operations for datasets and related tables in the DB
"""

import json

from db import ENGINE
from fastapi import APIRouter, Response, status
from generated import schema, orm
from logging import Logger, DEBUG
from sqlalchemy.orm import Session

logger = Logger(__file__)
# logger.setLevel(DEBUG)
router = APIRouter()


@router.get("/")
def get_person(count: int):
    with Session(ENGINE) as session:
        result = session.query(orm.Person).order_by(orm.Person.id.asc()).limit(count)
        result = result[::]
        return result


@router.get("/{id}")
def get_person(id: int) -> str:
    with Session(ENGINE) as session:
        result = session.query(orm.Person).get(id)
        logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_person(payload: schema.Person):
    with Session(ENGINE) as session:
        personp = payload.dict()
        person = orm.Person(**personp)
        session.add(person)
        session.commit()
        payload["id"] = person.id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/persons/{person.id}",
                "content-type": "application/json",
            },
            content=json.dumps(payload),
        )


@router.patch("/{id}")
def update_person(payload: schema.Person, id: int) -> str:
    with Session(ENGINE) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Person).filter(orm.Person.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Person"


@router.delete("/{id}")
def delete_person(id: int) -> str:
    with Session(ENGINE) as session:
        session.query(orm.Person).filter(orm.Person.id == id).delete()
        session.commit()
