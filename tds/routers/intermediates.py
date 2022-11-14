"""
tds.router.models - crud operations for models
"""

import json
from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
from tds.autogen.schema import RelationType
from tds.db import (
    ProvenanceHandler,
    entry_exists,
    request_provenance_handler,
    request_rdb,
)
from tds.operation import create, retrieve, update
from tds.schema.intermediate import Intermediate

logger = Logger(__name__)
router = APIRouter()


@router.get("")
def get_intermediates(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a count of persons
    """
    print(count)
    with Session(rdb) as session:
        return (
            session.query(orm.Intermediate)
            .order_by(orm.Intermediate.id.asc())
            .limit(count)
            .all()
        )


@router.get("/{id}", **retrieve.fastapi_endpoint_config)
def get_intermediate(id: int, rdb: Engine = Depends(request_rdb)) -> Intermediate:
    """
    Retrieve model
    """
    if entry_exists(rdb.connect(), orm.Intermediate, id):
        with Session(rdb) as session:
            Intermediate_ = session.query(orm.Intermediate).get(id)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Intermediate.from_orm(Intermediate_)


@router.post("", **create.fastapi_endpoint_config)
def create_intermediate(
    payload: Intermediate, rdb: Engine = Depends(request_rdb)
) -> dict:
    """
    Create intermediate and return its ID
    """
    with Session(rdb) as session:
        intermediate_payload = payload.dict()
        # pylint: disable-next=unused-variable
        intermediate_ = orm.Intermediate(**intermediate_payload)
        session.add(intermediate_)
        session.commit()
        id: int = intermediate_.id

    logger.info("new model created: %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "location": f"/api/intermediate/{id}",
            "content-type": "application/json",
        },
        content=json.dumps({"intermediate_id": id}),
    )
