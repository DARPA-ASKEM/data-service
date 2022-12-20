"""
CRUD operations for models
"""

import json
from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
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
from tds.schema.provenance import Provenance
from tds.settings import settings

logger = Logger(__name__)
router = APIRouter()


@router.post("/frameworks", **create.fastapi_endpoint_config)
def create_framework(
    payload: ModelFramework, rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Create framework metadata
    """

    with Session(rdb) as session:
        framework_payload = payload.dict()
        framework = orm.ModelFramework(**framework_payload)
        session.add(framework)
        session.commit()
        name: str = framework.name
    logger.info("new framework with %i", name)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"name": name}),
    )


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
            session.delete(intermediate)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.get("/descriptions")
def list_model_descriptions(
    page_size: int = 100, page: int = 0, rdb: Engine = Depends(request_rdb)
) -> List[Model]:

    """
    Retrieve all models

    This will return the full list of models, even the previous ones from
    edit history.
    """
    return list_by_id(rdb.connect(), orm.ModelDescription, page_size, page)


@router.get("/descriptions/{id}", **retrieve.fastapi_endpoint_config)
def get_model_description(
    id: int, rdb: Engine = Depends(request_rdb)
) -> ModelDescription:
    """
    Retrieve model
    """
    if entry_exists(rdb.connect(), orm.ModelDescription, id):
        with Session(rdb) as session:
            model = session.query(orm.ModelDescription).get(id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return ModelDescription.from_orm(model)


@router.get("/model_parameters/{id}", **retrieve.fastapi_endpoint_config)
def get_model_parameter(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Retrieve model parameter
    """
    with Session(rdb) as session:
        if (
            session.query(orm.ModelParameter)
            .filter(orm.ModelParameter.id == id)
            .count()
            == 1
        ):
            return session.query(orm.ModelParameter).get(id)
        raise HTTPException(status_code=status.HTTP_404_NOT_F)


@router.get("/parameters/{id}", **retrieve.fastapi_endpoint_config)
def get_model_parameters(
    id: int, rdb: Engine = Depends(request_rdb)
) -> ModelParameters:
    """
    Retrieve model
    """
    if entry_exists(rdb.connect(), orm.ModelDescription, id):
        with Session(rdb) as session:
            parameters: Query[orm.ModelParameter] = session.query(
                orm.ModelParameter
            ).filter(orm.ModelParameter.model_id == id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return orm_to_params(list(parameters))


@router.put("/parameters/{id}", **update.fastapi_endpoint_config)
def update_model_parameters(
    payload: ModelParameters, id: int, rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Update the parameters for a model
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
    if entry_exists(rdb.connect(), orm.ModelDescription, id):
        with Session(rdb) as session:
            model = session.query(orm.ModelDescription).get(id)
            content = session.query(orm.ModelState).get(model.state_id)
            parameters: List[orm.ModelParameter] = (
                session.query(orm.ModelParameter)
                .filter(orm.ModelParameter.model_id == id)
                .all()
            )

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Model.from_orm(model, content, parameters)


@router.post("", **create.fastapi_endpoint_config)
def create_model(
    payload: Model,
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> Response:
    """
    Create model and return its ID
    """
    with Session(rdb) as session:
        model_payload = payload.dict()
        model_payload.pop("concept")  # TODO: Save ontology term

        content = model_payload.pop("content")
        state = orm.ModelState(content=content)
        session.add(state)
        session.commit()
        model_payload["state_id"] = state.id

        parameters = model_payload.pop("parameters")
        model_payload.pop("id")

        model = orm.ModelDescription(**model_payload)
        session.add(model)
        session.commit()
        id: int = model.id
        for param in parameters:
            session.add(
                orm.ModelParameter(
                    model_id=id,
                    name=param["name"],
                    default_value=param["default_value"],
                    type=param["type"],
                    state_variable=param.get("state_variable", False),
                )
            )
        session.commit()
        if settings.NEO4J:
            print("Neo4j is set")
            # payload={"left":model.id,"left_type":"models","right":state.id,"right_type":"states","relationship_type":"BEGINS_AT"}
            provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
            payload = Provenance(
                left=model.id,
                left_type="models",
                right=state.id,
                right_type="model_revisions",
                relation_type="BEGINS_AT",
                user_id=model_payload.get("user_id", None),
            )

            provenance_handler.create_entry(payload)
    logger.info("new model created: %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )


@router.post("/{id}/copy", **create.fastapi_endpoint_config)
def copy_model(
    payload: dict,
    id: int,
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> Response:
    """
    Create model and return its ID
    """
    with Session(rdb) as session:
        old_model_id = id

        # query old model and old content
        model = session.query(orm.ModelDescription).get(old_model_id)
        framework = model.framework
        description = model.description
        name = model.name
        # set old state id so we have it
        old_state_id = model.state_id

        content = session.query(orm.ModelState).get(model.state_id)
        # take off content id so we can save it again in the database with new id
        content_payload = content.__dict__
        state = orm.ModelState(content=content_payload.get("content"))
        session.add(state)
        session.commit()

        new_state_id = state.id
        model = session.query(orm.ModelDescription).get(old_model_id)

        new_model = orm.ModelDescription(
            name=payload.get("name", name),
            description=payload.get("description", description),
            framework=framework,
            state_id=new_state_id,
        )
        session.add(new_model)
        session.commit()
        new_model_id = new_model.id

        parameters: List[orm.ModelParameter] = (
            session.query(orm.ModelParameter)
            .filter(orm.ModelParameter.model_id == old_model_id)
            .all()
        )

        # set the parameters as the same for copied model
        for param in parameters:
            session.add(
                orm.ModelParameter(
                    model_id=new_model_id,
                    name=param.name,
                    default_value=param.default_value,
                    type=param.type,
                    state_variable=param.state_variable,
                )
            )
        session.commit()

        if settings.NEO4J:
            provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
            prov_payload = Provenance(
                left=new_state_id,
                left_type="model_revisions",
                right=old_state_id,
                right_type="model_revisions",
                relation_type="COPIED_FROM",
                user_id=payload.get("user_id", None),
            )
            provenance_handler.create_entry(prov_payload)

            prov_payload = Provenance(
                left=new_model_id,
                left_type="models",
                right=new_state_id,
                right_type="model_revisions",
                relation_type="BEGINS_AT",
                user_id=payload.get("user_id", None),
            )
            provenance_handler.create_entry(prov_payload)

    logger.info("new model created: %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": new_model_id}),
    )


@router.post("/{id}", **update.fastapi_endpoint_config)
def update_model(
    payload: Model,
    id: int,
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> Response:
    """
    Update model content
    """
    # TODO: reinclude `provenance_handler = ProvenanceHandler(rdb, graph_db)`
    if entry_exists(rdb.connect(), orm.ModelDescription, id):
        model_payload = payload.dict()
        content = model_payload.pop("content")
        model_payload.pop("parameters")
        with Session(rdb) as session:
            state = orm.ModelState(content=content)
            session.add(state)
            session.commit()

            model = session.query(orm.ModelDescription).get(id)

            old_state = model.state_id

            model.state_id = state.id
            model.name = model_payload["name"]
            model.description = model_payload["description"]
            model.framework = model_payload["framework"]
            model.state_id = state.id
            session.commit()
            if settings.NEO4J:
                provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)

                payload = Provenance(
                    left=state.id,
                    left_type="model_revisions",
                    right=old_state,
                    right_type="model_revisions",
                    relation_type="EDITED_FROM",
                    user_id=model_payload.get("user_id", None),
                )
                provenance_handler.create_entry(payload)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )
