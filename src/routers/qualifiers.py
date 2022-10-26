"""
router.datasets - crud operations for datasets and related tables in the DB
"""

import api_schema
import datetime
import json

from db import ENGINE
from fastapi import APIRouter, Response, status
from generated import schema, orm
from logging import Logger, DEBUG
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import Dict, Any

logger = Logger(__file__)
# logger.setLevel(DEBUG)
router = APIRouter()


@router.get("/")
def get_qualifiers(count: int):
    with Session(ENGINE) as session:
        result = (
            session.query(orm.Dataset).order_by(orm.Qualifier.id.asc()).limit(count)
        )
        result = result[::]
        return result


@router.get("/{id}")
def get_qualifier(id: int) -> str:
    with Session(ENGINE) as session:
        result = session.query(orm.Qualifier).get(id)
        logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_qualifier(payload: api_schema.Qualifier):
    with Session(ENGINE) as session:
        qualifierp = payload.dict()
        qualifier = orm.Qualifier(**qualifierp)
        session.add(qualifier)
        session.commit()
        payload["id"] = qualifier.id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/qualifiers/{qualifier.id}",
                "content-type": "application/json",
            },
            content=json.dumps(payload),
        )


@router.patch("/{id}")
def update_qualifier(payload: schema.Qualifier, id: int) -> str:
    with Session(ENGINE) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Qualifier).filter(orm.Qualifier.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Qualifier"


@router.delete("/{id}")
def delete_qualifier(id: int) -> str:
    with Session(ENGINE) as session:
        session.query(orm.Qualifier).filter(orm.Qualifier.id == id).delete()
        session.commit()
