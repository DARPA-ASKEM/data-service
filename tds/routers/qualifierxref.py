"""
router.qualifier xrefs - crud operations for qualifier xrefs and
related tables in the DB
"""

import json
from logging import Logger

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import request_rdb

logger = Logger(__file__)
# logger.setLevel(DEBUG)
router = APIRouter()


@router.get("/")
def get_qualifier_xrefs(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a specified number of qualifier xrefs
    """
    with Session(rdb) as session:
        result = (
            session.query(orm.QualifierXref)
            .order_by(orm.QualifierXref.id.asc())
            .limit(count)
        )
        result = result[::]
        return result


@router.get("/{id}")
def get_qualifier_xref(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific qualifier xref by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.QualifierXref).get(id)
        # logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_qualifier_xref(
    payload: schema.QualifierXref, rdb: Engine = Depends(request_rdb)
):
    """
    Create a qualifier xref
    """
    create_xref_component(payload, rdb)


@router.patch("/{id}")
def update_qualifier_xref(
    payload: schema.Qualifier, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Update a qualifier xref by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.QualifierXref).filter(
            orm.QualifierXref.id == id
        )
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Qualifier xref"


@router.delete("/{id}")
def delete_qualifier_xref(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Delete a qualifier xref by ID
    """
    with Session(rdb) as session:
        session.query(orm.QualifierXref).filter(orm.QualifierXref.id == id).delete()
        session.commit()


# Has to be separate so that the qualifiers router can use this
# function inside of the API.
def create_xref_component(payload: schema.QualifierXref, rdb: Engine):
    """
    Function to create an xref component that can also be used internally.
    """
    with Session(rdb) as session:
        qualifier_xrefp = {}
        try:
            qualifier_xrefp = payload.dict()
        except TypeError as error:
            logger.error(error)
            qualifier_xrefp = payload
        del qualifier_xrefp["id"]
        qualifier_xref = orm.QualifierXref(**qualifier_xrefp)
        exists = (
            session.query(orm.QualifierXref).filter_by(**qualifier_xrefp).first()
            is not None
        )
        if exists:
            return Response(
                status_code=status.HTTP_200_OK,
                headers={
                    "location": "/api/qualifierxref/",
                    "content-type": "application/json",
                },
                content=json.dumps(qualifier_xrefp),
            )

        session.add(qualifier_xref)
        session.commit()
        data_id = qualifier_xref.id
        qualifier_xrefp["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/qualifier_xrefs/{data_id}",
                "content-type": "application/json",
            },
            content=json.dumps(qualifier_xrefp),
        )
