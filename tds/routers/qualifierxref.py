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
from typing import Dict, Any

logger = Logger(__file__)
# logger.setLevel(DEBUG)
router = APIRouter()


@router.get("/")
def get_qualifer_xrefs(count: int, rdb: Engine = Depends(request_rdb)):
    with Session(rdb) as session:
        result = (
            session.query(orm.QualifierXref)
            .order_by(orm.QualifierXref.id.asc())
            .limit(count)
        )
        result = result[::]
        return result


@router.get("/{id}")
def get_qualifer_xref(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    with Session(rdb) as session:
        result = session.query(orm.QualifierXref).get(id)
        logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_qualifer_xref(
    payload: schema.QualifierXref, rdb: Engine = Depends(request_rdb)
):

    create_xref_function(payload, rdb)


@router.patch("/{id}")
def update_qualifer_xref(
    payload: schema.Qualifier, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.QualifierXref).filter(
            orm.QualiferXref.id == id
        )
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Qualifier xref"


@router.delete("/{id}")
def delete_qualifer_xref(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    with Session(rdb) as session:
        session.query(orm.QualifierXref).filter(orm.QualifierXref.id == id).delete()
        session.commit()


# Has to be separate so that the qualifiers router can use this function inside of the API.
def create_xref_component(payload: schema.QualifierXref, rdb: Engine):
    with Session(rdb) as session:
        qualifer_xrefp = {}
        try:
            qualifer_xrefp = payload.dict()
        except:
            qualifer_xrefp = payload
        del qualifer_xrefp["id"]
        qualifer_xref = orm.QualifierXref(**qualifer_xrefp)
        session.add(qualifer_xref)
        session.commit()
        data_id = qualifer_xref.id
        qualifer_xrefp["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/qualifer_xrefs/{data_id}",
                "content-type": "application/json",
            },
            content=json.dumps(qualifer_xrefp),
        )
