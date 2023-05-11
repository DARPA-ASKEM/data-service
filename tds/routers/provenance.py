"""

Create, Delete and Search operations for Provenance

"""

import json
from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import ProvenanceHandler, SearchProvenance, request_graph_db, request_rdb
from tds.operation import create, delete, retrieve
from tds.schema.provenance import Provenance, ProvenancePayload

logger = Logger(__name__)
router = APIRouter()


@router.get("", **retrieve.fastapi_endpoint_config)
def get_provenance(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Searches for a provenance entry in TDS
    """
    with Session(rdb) as session:
        return Provenance.from_orm(session.query(orm.Provenance).get(id))


@router.post("/search")
def search_provenance(
    payload: ProvenancePayload,
    search_type: schema.ProvenanceSearchTypes = Query(
        default=schema.ProvenanceSearchTypes.connected_nodes
    ),
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> Response:
    """
    Search provenance of for all artifacts that helped derive this artifact.

    ## Types of searches:

    **artifacts_created_by_user** - Return all artifacts created by a user.
    * Requirements: “user_id”

    **child_nodes** - Returns all child nodes of this artifact.
    (In other words artifacts created after this artifact
     that were dependent/derived from the root artifact).
    * Requirements: “root_type”, “root_id”


    **parent_nodes** - Return all parent nodes of this artifact.
    (Artifacts created before this artifact that help
    derive/create this root artifact).
    * Requirements: “root_type”, “root_id”

    **connected_nodes** - Return all parent and child nodes
     of this artifact.
    * Requirements: “root_type”, “root_id”


    **derived_models** - Return all models that were derived
        from a publication or intermediate.
    * Requirements: “root_type”, “root_id”
    * Allowed root _types are Publication and Intermediate


    **parent_model_revisions** - Returns the model revisions
    that helped create the model that was used to create the root artifact.
    * Requirements: “root_type”, “root_id”
    * Allowed root _types are Model, Plan, SimulationRun, and Dataset


    **parent_models** - Returns the models that helped create
     the model that was used to create the root artifact.
    * Requirements: “root_type”, “root_id”
    * Allowed root _types are Model *will be expanded.

    ## Payload format

    The payload for searching needs to match the schema below.

    Provenance Types are :
    Dataset, Model, ModelParameter, Plan, PlanParameter, ModelRevision, Intermediate,
    Publication, SimulationRun, Project, Concept.


    ***edges*** set to true: edges will be returned if found

    ***nodes*** set to true: nodes will not be returned if found

    ***types*** filters node types you want returned.

    ***hops*** limits the number of relationships away from
    the root node the search will traverse.

    ***limit*** will limit the number of nodes returned for relationship and nodes.
      The closest n number of nodes to the root node will be returned. There might
      not be the exact the number of nodes returned as requested due to filtering
      out node types.

    ***versions*** set to true will return model revisions in edges. Versions set to
     false will squash all model revisions to the
     Model node they are associated with along with all the relationships connected
     to model revisions

        {
            "root_id": 1,
            "root_type": "Publication",
            "curie": "string",
            "edges": false,
            "nodes": true,
            "types": [
                "Dataset",
                "Intermediate",
                "Model",
                "ModelParameter",
                "Plan",
                "PlanParameter",
                "Publication",
                "SimulationRun"
            ],
            "hops": 15,
            "limit": 1000,
            "versions": false
        }

    """
    logger.info("Search provenance")
    payload = payload.__dict__
    search_provenance_handler = SearchProvenance(rdb=rdb, graph_db=graph_db)
    search_function = search_provenance_handler[search_type]
    results = search_function(payload=payload)

    return Response(
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"result": results}),
    )


@router.post("", **create.fastapi_endpoint_config)
def create_provenance(
    payload: Provenance,
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> Response:
    """
    Create provenance relationship
    """

    provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
    id: int = provenance_handler.create_entry(payload)

    logger.info("new provenance with %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )


@router.delete("/hanging_nodes")
def delete_hanging_nodes(
    rdb: Engine = Depends(request_rdb), graph_db=Depends(request_graph_db)
) -> Response:
    """
    Prunes nodes that have 0 edges
    """
    provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
    success = provenance_handler.delete_nodes()
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"success": success}),
    )


@router.delete("/{id}", **delete.fastapi_endpoint_config)
def delete_provenance(
    id: int,
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> Response:
    """
    Delete provenance metadata
    """
    with Session(rdb) as session:
        if session.query(orm.Provenance).filter(orm.Provenance.id == id).count() == 1:
            provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
            success = provenance_handler.delete(id=id)

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id, "success": success}),
    )
