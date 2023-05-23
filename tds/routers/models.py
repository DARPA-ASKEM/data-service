"""
CRUD operations for models
"""

import json
from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm, schema
from tds.db import ProvenanceHandler, request_graph_db, request_rdb
from tds.lib.models import model_opt_relationship_mapping
from tds.operation import create, delete, retrieve
from tds.schema.model import ModelFramework, ModelOptPayload, orm_to_params
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


@router.post("/opts/{model_operation}", **create.fastapi_endpoint_config)
def model_opt(
    payload: ModelOptPayload,
    model_operation: schema.ModelOperations,
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> Response:
    """
    Make modeling operations.
    """
    with Session(rdb) as session:
        payload = payload.dict()
        l_model = session.query(orm.ModelDescription).get(payload.get("left"))
        if payload.get("right", False):
            r_model = session.query(orm.ModelDescription).get(payload.get("right"))

        if model_operation == "copy":
            state = orm.ModelState(
                content=session.query(orm.ModelState)
                .get(payload.get("left"))
                .__dict__.get("content")
            )

        elif model_operation in ("decompose", "glue"):
            state = orm.ModelState(content=payload.get("content"))
        else:
            raise HTTPException(status_code=400, detail="Operation not supported")

        session.add(state)
        session.commit()

        # add new model
        new_model = orm.ModelDescription(
            name=payload.get("name"),
            description=payload.get("description"),
            framework=payload.get("framework"),
            state_id=state.id,
        )
        session.add(new_model)
        session.commit()

        # add parameters to new model. Default to left model id parameters.
        if payload.get("parameters") is None:
            parameters: List[dict] = (
                session.query(orm.ModelParameter)
                .filter(orm.ModelParameter.model_id == payload.get("left"))
                .all()
            )
            payload["parameters"] = []
            for parameter in parameters:
                payload["parameters"].append(parameter.__dict__)

        for param in payload.get("parameters"):
            session.add(
                orm.ModelParameter(
                    model_id=new_model.id,
                    name=param.get("name"),
                    default_value=param.get("default_value"),
                    type=param.get("type"),
                    state_variable=param.get("state_variable"),
                )
            )
        session.commit()

        if settings.NEO4J_ENABLED:
            provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
            prov_payload = Provenance(
                left=state.id,
                left_type="ModelRevision",
                right=l_model.state_id,
                right_type="ModelRevision",
                relation_type=model_opt_relationship_mapping[model_operation],
                user_id=payload.get("user_id", None),
                concept=".",
            )
            provenance_handler.create_entry(prov_payload)

            if model_operation == "glue" and payload.get("right", False):
                prov_payload = Provenance(
                    left=state.id,
                    left_type="ModelRevision",
                    right=r_model.state_id,
                    right_type="ModelRevision",
                    relation_type=model_opt_relationship_mapping[model_operation],
                    user_id=payload.get("user_id", None),
                    concept=".",
                )
                provenance_handler.create_entry(prov_payload)

            # add begins at relationship
            prov_payload = Provenance(
                left=new_model.id,
                left_type="Model",
                right=state.id,
                right_type="ModelRevision",
                relation_type="BEGINS_AT",
                user_id=payload.get("user_id", None),
                concept=".",
            )
            provenance_handler.create_entry(prov_payload)

            # get recently added parameters for the new model
            parameters: Query[orm.ModelParameter] = session.query(
                orm.ModelParameter
            ).filter(orm.ModelParameter.model_id == new_model.id)

            created_parameters = orm_to_params(list(parameters))
            # add ModelParameter nodes
            for parameter in created_parameters:
                payload = Provenance(
                    left=parameter.get("id"),
                    left_type="ModelParameter",
                    right=new_model.state_id,
                    right_type="ModelRevision",
                    relation_type="PARAMETER_OF",
                    user_id=None,
                    concept=".",
                )
                provenance_handler.create_entry(payload)

    logger.info("new model created: %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": new_model.id}),
    )
