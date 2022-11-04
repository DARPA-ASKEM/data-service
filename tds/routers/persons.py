"""
router.datasets - crud operations for datasets and related tables in the DB
"""

import json

from tds.db import request_rdb
from sqlalchemy.engine.base import Engine
from fastapi import APIRouter, Depends, Response, status
from tds.autogen import schema, orm
from logging import Logger, DEBUG
from sqlalchemy.orm import Session

logger = Logger(__file__)
# logger.setLevel(DEBUG)
router = APIRouter()


@router.get("/")
def get_person(count: int, rdb: Engine = Depends(request_rdb)):
    with Session(rdb) as session:
        result = session.query(orm.Person).order_by(orm.Person.id.asc()).limit(count)
        result = result[::]
        return result


@router.get("/{id}")
def get_person(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    with Session(rdb) as session:
        result = session.query(orm.Person).get(id)
        logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_person(payload: schema.Person, rdb: Engine = Depends(request_rdb)):
    with Session(rdb) as session:
        personp = payload.dict()
        del personp["id"]
        person = orm.Person(**personp)
        session.add(person)
        session.commit()
        data_id = person.id
        personp["id"] = data_id
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
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Person).filter(orm.Person.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Person"


@router.delete("/{id}")
def delete_person(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    with Session(rdb) as session:
        session.query(orm.Person).filter(orm.Person.id == id).delete()
        session.commit()
