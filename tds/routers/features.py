"""
router.datasets - crud operations for datasets and related tables in the DB
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
def get_features(count: int, rdb: Engine = Depends(request_rdb)):
    with Session(rdb) as session:
        result = session.query(orm.Feature).order_by(orm.Feature.id.asc()).limit(count)
        result = result[::]
        return result


@router.get("/{id}")
def get_feature(id: int) -> str:
    with Session(rdb) as session:
        result = session.query(orm.Feature).get(id)
        logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_feature(payload: schema.Feature, rdb: Engine = Depends(request_rdb)):
    with Session(rdb) as session:
        featurep = payload.dict()
        del featurep["id"]
        feature = orm.Feature(**featurep)
        exists = session.query(orm.Feature).filter_by(**featurep).first() is not None
        if exists:
            return Response(
                status_code=status.HTTP_200_OK,
                headers={
                    "location": f"/api/features/",
                    "content-type": "application/json",
                },
                content=json.dumps(featurep),
            )
        session.add(feature)
        session.commit()
        data_id = feature.id
        featurep["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/features/{data_id}",
                "content-type": "application/json",
            },
            content=json.dumps(featurep),
        )


@router.patch("/{id}")
def update_feature(
    payload: schema.Feature, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Feature).filter(orm.Feature.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Feature"


@router.delete("/{id}")
def delete_feature(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    with Session(rdb) as session:
        session.query(orm.Feature).filter(orm.Feature.id == id).delete()
        session.commit()
