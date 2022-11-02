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
def get_association(count: int):
    with Session(ENGINE) as session:
        result = (
            session.query(orm.Association)
            .order_by(orm.Association.id.asc())
            .limit(count)
        )
        result = result[::]
        return result


@router.get("/{id}")
def get_association(id: int) -> str:
    with Session(ENGINE) as session:
        result = session.query(orm.Association).get(id)
        logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_association(payload: schema.Association):
    with Session(ENGINE) as session:
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
def update_association(payload: schema.Association, id: int) -> str:
    with Session(ENGINE) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Association).filter(orm.Association.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated association"


@router.delete("/{id}")
def delete_association(id: int) -> str:
    with Session(ENGINE) as session:
        session.query(orm.Association).filter(orm.Association.id == id).delete()
        session.commit()
