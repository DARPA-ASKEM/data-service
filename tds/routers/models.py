"""
router.models - crud operations for models
"""

from logging import Logger

from fastapi import APIRouter, Depends
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.autogen.schema import RelationType
from tds.db import request_rdb
from tds.operation import create, retrieve, update
from tds.relation.provenance import RelationHandler, request_relation_handler
from tds.schema.model import Model

logger = Logger(__name__)
router = APIRouter()


@router.get("/{id}", **retrieve.fastapi_endpoint_config)
def get_model(id: int, rdb: Engine = Depends(request_rdb)) -> Model:
    """
    Retrieve model
    """
    with Session(rdb) as session:
        model = session.query(orm.Model).get(id)
        return Model.from_orm(model)


@router.post("", **create.fastapi_endpoint_config)
def create_model(payload: Model, rdb: Engine = Depends(request_rdb)) -> int:
    """
    Create model and return its ID
    """
    with Session(rdb) as session:
        model_payload = payload.dict()
        # pylint: disable-next=unused-variable
        concept_payload = model_payload.pop("concept")  # TODO: Save ontology term
        model = orm.Model(**model_payload)
        session.add(model)
        session.commit()
        id: int = model.id
    logger.info("new model created: %i", id)
    return id


@router.post("/{id}", **update.fastapi_endpoint_config)
def update_model(
    payload: Model,
    id: int,
    rdb: Engine = Depends(request_rdb),
    relation_handler: RelationHandler = Depends(request_relation_handler),
) -> Model:
    """
    Update model content
    """
    with Session(rdb) as session:
        model_payload = payload.dict()
        # pylint: disable-next=unused-variable
        concept_payload = model_payload.pop("concept")  # TODO: Save ontology term
        model_payload["id"] = None
        model = orm.Model(**model_payload)
        session.add(model)
        session.commit()
        old_model = session.query(orm.Model).get(id)
    relation_handler.create(
        Model.from_orm(model), Model.from_orm(old_model), RelationType.editedFrom
    )
    return get_model(id)
