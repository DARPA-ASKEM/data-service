"""
CRUD operations for models
"""

import json
from logging import Logger
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from neo4j import Driver
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
from tds.autogen.schema import RelationType
from tds.db import (
    ProvenanceHandler,
    entry_exists,
    list_by_id,
    request_graph_db,
    request_rdb,
)
from tds.lib.models import adjust_model_params
from tds.operation import create, delete, retrieve, update
from tds.schema.model import (
    Intermediate,
    Model,
    ModelDescription,
    ModelFramework,
    ModelParameters,
    orm_to_params,
)

logger = Logger(__name__)
router = APIRouter()


@router.post("/frameworks", **create.fastapi_endpoint_config)
def create_framework(
    payload: ModelFramework, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Create framework metadata
    """

    with Session(rdb) as session:
        framework_payload = payload.dict()
        framework = orm.ModelFramework(**framework_payload)
        session.add(framework)
        session.commit()
    logger.info("new framework with %i", framework_payload.get("name"))
    return framework_payload.get("name")


@router.get("/frameworks/{name}", **retrieve.fastapi_endpoint_config)
def get_framework(name: str, rdb: Engine = Depends(request_rdb)) -> ModelFramework:
    """
    Retrieve framework metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.ModelFramework)
            .filter(orm.ModelFramework.name == name)
            .count()
            == 1
        ):
            return ModelFramework.from_orm(session.query(orm.ModelFramework).get(name))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/frameworks/{name}", **delete.fastapi_endpoint_config)
def delete_framework(name: str, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Delete framework metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.ModelFramework)
            .filter(orm.ModelFramework.name == name)
            .count()
            == 1
        ):
            framework = session.query(orm.ModelFramework).get(name)
            session.delete(framework)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.get("/intermediates/{id}", **retrieve.fastapi_endpoint_config)
def get_intermediate(id: int, rdb: Engine = Depends(request_rdb)) -> Intermediate:
    """
    Retrieve model
    """
    if entry_exists(rdb.connect(), orm.Intermediate, id):
        with Session(rdb) as session:
            intermediate = session.query(orm.Intermediate).get(id)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Intermediate.from_orm(intermediate)


@router.post("/intermediates", **create.fastapi_endpoint_config)
def create_intermediate(
    payload: Intermediate, rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Create intermediate and return its ID
    """
    with Session(rdb) as session:
        intermediate_payload = payload.dict()
        # pylint: disable-next=unused-variable
        intermediate = orm.Intermediate(**intermediate_payload)
        session.add(intermediate)
        session.commit()
        id: int = intermediate.id

    logger.info("new model created: %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )


@router.delete("/intermediates/{id}", **delete.fastapi_endpoint_config)
def delete_intermediate(id: int, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Delete framework metadata
    """
    with Session(rdb) as session:
        if entry_exists(rdb.connect(), orm.Intermediate, id):
            intermediate = session.query(orm.Intermediate).get(id)
            print(intermediate)
            session.delete(intermediate)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.get("/descriptions")
def list_model_descriptions(
    page: int = 100, page_size: int = 0, rdb: Engine = Depends(request_rdb)
) -> List[Model]:
    """
    Retrieve all models

    This will return the full list of models, even the previous ones from
    edit history.
    """
    return list_by_id(rdb.connect(), orm.Model, page, page_size)


@router.get("/descriptions/{id}", **retrieve.fastapi_endpoint_config)
def get_model_description(
    id: int, rdb: Engine = Depends(request_rdb)
) -> ModelDescription:
    """
    Retrieve model
    """
    if entry_exists(rdb.connect(), orm.Model, id):
        with Session(rdb) as session:
            model = session.query(orm.Model).get(id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return ModelDescription.from_orm(model)


@router.get("/parameters/{id}", **retrieve.fastapi_endpoint_config)
def get_model_parameters(
    id: int, rdb: Engine = Depends(request_rdb)
) -> ModelParameters:
    """
    Retrieve model
    """
    if entry_exists(rdb.connect(), orm.Model, id):
        with Session(rdb) as session:
            parameters: Query[orm.ModelParameter] = session.query(
                orm.ModelParameter
            ).filter(orm.ModelParameter.model_id == id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return orm_to_params(list(parameters))


@router.put("/parameters/{id}", **update.fastapi_endpoint_config)
def update_run_parameters(
    payload: ModelParameters, id: int, rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Update the parameters for a run
    """
    with Session(rdb) as session:
        adjust_model_params(id, payload, session)
        session.commit()
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
    )


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
def create_model(payload: Model, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Create model and return its ID
    """
    with Session(rdb) as session:
        model_payload = payload.dict()
        model_payload.pop("concept")  # TODO: Save ontology term
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
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )


@router.post("/{id}", **update.fastapi_endpoint_config)
def update_model(
    payload: Model,
    id: int,
    rdb: Engine = Depends(request_rdb),
    graph_db: Optional[Driver] = Depends(request_graph_db),
) -> Response:
    """
    Update model content
    """
    provenance_handler = ProvenanceHandler(rdb, graph_db)
    if entry_exists(rdb.connect(), orm.Model, id):
        new_id = json.loads(create_model(payload, rdb).body)["id"]
        old_model = get_model(id, rdb)
        new_model = get_model(new_id, rdb)
        provenance_handler.create(new_model, old_model, RelationType.editedFrom)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": new_id}),
    )
