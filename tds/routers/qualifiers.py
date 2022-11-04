"""
router.datasets - crud operations for datasets and related tables in the DB
"""

import datetime
import json

from tds.db import request_rdb
from sqlalchemy.engine.base import Engine
from fastapi import APIRouter, Depends, Response, status
from tds.autogen import schema, orm
from logging import Logger, DEBUG
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from tds.routers.qualifierxref import create_xref_component

logger = Logger(__file__)
# logger.setLevel(DEBUG)
router = APIRouter()


@router.get("/")
def get_qualifiers(count: int, rdb: Engine = Depends(request_rdb)):
    with Session(rdb) as session:
        result = (
            session.query(orm.Qualifier).order_by(orm.Qualifier.id.asc()).limit(count)
        )
        result = result[::]
        return result


@router.get("/{id}")
def get_qualifier(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    with Session(rdb) as session:
        result = session.query(orm.Qualifier).get(id)
        logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_qualifier(
    payload: schema.Qualifier,
    qualifies_array: List[str],
    rdb: Engine = Depends(request_rdb),
):
    with Session(rdb) as session:
        qualifierp = payload.dict()
        del qualifierp["id"]
        qualifier = orm.Qualifier(**qualifierp)
        session.add(qualifier)
        session.commit()
        data_id = qualifier.id
        for q in qualifies_array:
            feature = (
                session.query(orm.Feature)
                .filter_by(name=q, dataset_id=qualifierp["dataset_id"])
                .first()
            )
            qualifier_xrefp = {
                "id": 0,
                "qualifier_id": data_id,
                "feature_id": feature.id,
            }
            create_xref_component(qualifier_xrefp, rdb)
        qualifierp["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/qualifiers/{data_id}",
                "content-type": "application/json",
            },
            content=json.dumps(qualifierp),
        )


@router.patch("/{id}")
def update_qualifier(
    payload: schema.Qualifier, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Qualifier).filter(orm.Qualifier.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Qualifier"


@router.delete("/{id}")
def delete_qualifier(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    with Session(rdb) as session:
        session.query(orm.Qualifier).filter(orm.Qualifier.id == id).delete()
        session.commit()
