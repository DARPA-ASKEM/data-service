"""
router.associations - crud operations for associations and related tables in the DB
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
def get_association(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a specific number of associations
    """
    with Session(rdb) as session:
        result = (
            session.query(orm.Association)
            .order_by(orm.Association.id.asc())
            .limit(count)
        )
        result = result[::]
        return result


@router.get("/{id}")
def get_association(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific association by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Association).get(id)
        # logger.info(f"Latest output: {result}")
        return result


@router.post("/")
def create_association(payload: schema.Association, rdb: Engine = Depends(request_rdb)):
    """
    Create a association
    """
    with Session(rdb) as session:
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
def update_association(
    payload: schema.Association, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Update a association by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Association).filter(orm.Association.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated association"


@router.delete("/{id}")
def delete_association(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Delete a association by ID
    """
    with Session(rdb) as session:
        session.query(orm.Association).filter(orm.Association.id == id).delete()
        session.commit()
