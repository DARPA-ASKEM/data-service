"""
CRUD operations for models
"""

import json
from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import and_
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db import request_rdb
from tds.lib.concepts import mark_concept_active
from tds.operation import create, retrieve
from tds.schema.parameter import IndependentParameter

logger = Logger(__name__)
router = APIRouter()


@router.post("", deprecated=True, **create.fastapi_endpoint_config)
def create_parameters(
    payload: List[IndependentParameter], rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Create parameters from a list
    """

    with Session(rdb) as session:
        created_ids = []
        for parameter_payload in [parameter.dict() for parameter in payload]:
            curie = parameter_payload.pop("curie")
            param = orm.ModelParameter(**parameter_payload)
            session.add(param)
            session.commit()
            if curie is not None:
                mark_concept_active(session, curie)
                concept = orm.OntologyConcept(
                    curie=curie,
                    type=orm.TaggableType.model_parameters,
                    object_id=param.id,
                    status=orm.OntologicalField.obj,
                )
                session.add(concept)
                session.commit()
                id: int = param.id
                logger.info("new parameter with %i", id)
                created_ids.append(id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"ids": created_ids}),
    )


@router.get("", deprecated=True, **retrieve.fastapi_endpoint_config)
def get_parameters(
    rdb: Engine = Depends(request_rdb), page: int = 0, page_size: int = 100
) -> List[IndependentParameter]:
    """
    Retrieve parameters
    """

    with Session(rdb) as session:
        query = (
            session.query(orm.ModelParameter, orm.OntologyConcept)
            .outerjoin(
                orm.OntologyConcept,
                and_(
                    orm.OntologyConcept.object_id == orm.ModelParameter.id,
                    orm.OntologyConcept.type == orm.TaggableType.model_parameters,
                ),
            )
            .order_by(orm.ModelParameter.id.asc())
            .limit(page_size)
            .offset(page * page_size)
            .all()
        )

    return [
        IndependentParameter(
            curie=concept.curie if concept is not None else None, **param.__dict__
        )
        for param, concept in query
    ]
