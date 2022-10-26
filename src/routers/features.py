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
def get_features(count: int):
    with Session(ENGINE) as session:
        result = session.query(orm.Dataset).order_by(orm.Feature.id.asc()).limit(count)
        result = result[::]
        return result


@router.get("/{id}")
def get_feature(id: int) -> str:
    with Session(ENGINE) as session:
        result = session.query(orm.Feature).get(id)
        logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_feature(payload: api_schema.Feature):
    with Session(ENGINE) as session:
        featurep = payload.dict()
        feature = orm.Feature(**featurep)
        session.add(feature)
        session.commit()
        payload["id"] = feature.id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/features/{feature.id}",
                "content-type": "application/json",
            },
            content=json.dumps(payload),
        )


@router.patch("/{id}")
def update_feature(payload: schema.Feature, id: int) -> str:
    with Session(ENGINE) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Feature).filter(orm.Feature.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Feature"


@router.delete("/{id}")
def delete_feature(id: int) -> str:
    with Session(ENGINE) as session:
        session.query(orm.Feature).filter(orm.Feature.id == id).delete()
        session.commit()
