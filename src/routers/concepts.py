"""
router.datasets - crud operations for datasets and related tables in the DB
"""

import api_schema
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
def get_concepts(count: int):
    with Session(ENGINE) as session:
        result = session.query(orm.Concept).order_by(orm.Concept.id.asc()).limit(count)
        result = result[::]
        return result


@router.get("/{id}")
def get_concept(id: int) -> str:
    with Session(ENGINE) as session:
        result = session.query(orm.Concept).get(id)
        logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_concept(payload: api_schema.Concept):
    with Session(ENGINE) as session:
        conceptp = payload.dict()
        del conceptp["id"]
        concept = orm.Concept(**conceptp)
        session.add(concept)
        session.commit()
        data_id = concept.id
        conceptp["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/concepts/{data_id}",
                "content-type": "application/json",
            },
            content=json.dumps(conceptp),
        )


@router.patch("/{id}")
def update_concept(payload: schema.Concept, id: int) -> str:
    with Session(ENGINE) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Concept).filter(orm.Concept.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Concept"


@router.delete("/{id}")
def delete_concept(id: int) -> str:
    with Session(ENGINE) as session:
        session.query(orm.Concept).filter(orm.Concept.id == id).delete()
        session.commit()
