"""
tds.router.models - crud operations for models
"""

from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
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
from tds.schema.model import Model

logger = Logger(__name__)
router = APIRouter()


@router.get("")
def list_models(rdb: Engine = Depends(request_rdb)) -> List[Model]:
    """
    Retrieve all models

    This will return the full list of models, even the previous ones from
    edit history.
    """
    results = []
    with Session(rdb) as session:
        for entry in session.query(orm.Model).all():
            parameters: Query[orm.ModelParameter] = session.query(
                orm.ModelParameter
            ).filter(orm.ModelParameter.model_id == entry.id)
            results.append(Model.from_orm(entry, list(parameters)))
    return results


@router.get("/{id}", **retrieve.fastapi_endpoint_config)
def get_model(id: int, rdb: Engine = Depends(request_rdb)) -> Model:
    """
    Retrieve model
    """
    if entry_exists(rdb.connect(), orm.Model, id):
        with Session(rdb) as session:
            model = session.query(orm.Model).get(id)
            parameters: Query[orm.ModelParameter] = session.query(
                orm.ModelParameter
            ).filter(orm.ModelParameter.model_id == id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Model.from_orm(model, list(parameters))


@router.post("", **create.fastapi_endpoint_config)
def create_model(payload: Model, rdb: Engine = Depends(request_rdb)) -> int:
    """
    Create model and return its ID
    """
    with Session(rdb) as session:
        model_payload = payload.dict()
        # pylint: disable-next=unused-variable
        concept_payload = model_payload.pop("concept")  # TODO: Save ontology term
        parameters = model_payload.pop("parameters")
        model_payload.pop("id")
        model = orm.Model(**model_payload)
        session.add(model)
        session.commit()
        id: int = model.id
        for name, type in parameters.items():
            session.add(orm.ModelParameter(model_id=id, name=name, type=type))
        session.commit()
    logger.info("new model created: %i", id)
    return id


@router.post("/{id}", **update.fastapi_endpoint_config)
def update_model(
    payload: Model,
    id: int,
    rdb: Engine = Depends(request_rdb),
    provenance_handler: ProvenanceHandler = Depends(request_provenance_handler),
) -> int:
    """
    Update model content
    """
    if entry_exists(rdb.connect(), orm.Model, id):
        new_id = create_model(payload, rdb)
        old_model = get_model(id, rdb)
        new_model = get_model(new_id, rdb)
        provenance_handler.create(new_model, old_model, RelationType.editedFrom)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return new_model.id
