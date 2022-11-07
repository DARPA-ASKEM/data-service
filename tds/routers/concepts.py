"""
router.concepts - crud operations for concepts and related tables in the DB
"""

import json
from logging import DEBUG, Logger

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import request_rdb

logger = Logger(__file__)
# logger.setLevel(DEBUG)
router = APIRouter()


@router.get("/")
def get_concepts(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a specific number of concepts
    """
    with Session(rdb) as session:
        result = session.query(orm.Concept).order_by(orm.Concept.id.asc()).limit(count)
        result = result[::]
        return result


@router.get("/{id}")
def get_concept(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific concept by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Concept).get(id)
        # logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_concept(payload: schema.Concept, rdb: Engine = Depends(request_rdb)):
    """
    Create a concept
    """
    with Session(rdb) as session:
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
def update_concept(
    payload: schema.Concept, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Update a concept by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Concept).filter(orm.Concept.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Concept"


@router.delete("/{id}")
def delete_concept(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Delete a concept by ID
    """
    with Session(rdb) as session:
        session.query(orm.Concept).filter(orm.Concept.id == id).delete()
        session.commit()
