"""
router.qualifiers - crud operations for qualifiers and related tables in the DB
"""

import json
from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import request_rdb
from tds.routers.qualifierxref import create_xref_component

logger = Logger(__file__)
# logger.setLevel(DEBUG)
router = APIRouter()


@router.get("/")
def get_qualifiers(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a specific number of qualifiers
    """
    with Session(rdb) as session:
        result = (
            session.query(orm.Qualifier).order_by(orm.Qualifier.id.asc()).limit(count)
        )
        result = result[::]
        return result


@router.get("/{id}")
def get_qualifier(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific qualifier by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Qualifier).get(id)
        # logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_qualifier(
    payload: schema.Qualifier,
    qualifies_array: List[str],
    rdb: Engine = Depends(request_rdb),
):
    """
    Create a qualifier
    """
    with Session(rdb) as session:
        qualifierp = payload.dict()
        del qualifierp["id"]
        qualifier = orm.Qualifier(**qualifierp)
        exists = (
            session.query(orm.Qualifier).filter_by(**qualifierp).first() is not None
        )
        if exists:
            return Response(
                status_code=status.HTTP_200_OK,
                headers={
                    "location": "/api/qualfiers/",
                    "content-type": "application/json",
                },
                content=json.dumps(qualifierp),
            )

        session.add(qualifier)
        session.commit()
        data_id = qualifier.id
        for qual in qualifies_array:
            feature = (
                session.query(orm.Feature)
                .filter_by(name=qual, qualifier_id=qualifierp["qualifier_id"])
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
    """
    Update a qualifier by ID
    """
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
    """
    Delete a qualifier by ID
    """
    with Session(rdb) as session:
        session.query(orm.Qualifier).filter(orm.Qualifier.id == id).delete()
        session.commit()
