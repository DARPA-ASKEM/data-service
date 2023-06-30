"""
    TDS Provenance Controller.

    Description: Defines the basic rest endpoints for the TDS Module.
"""
from logging import Logger

from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from tds.autogen import enums
from tds.db import request_graph_db, request_rdb
from tds.db.graph.provenance_handler import ProvenanceHandler
from tds.db.graph.search_provenance import SearchProvenance
from tds.modules.provenance.model import Provenance, ProvenancePayload, ProvenanceSearch
from tds.modules.provenance.response import ProvenanceResponse
from tds.operation import create, delete, retrieve

provenance_router = APIRouter()
logger = Logger(__name__)


@provenance_router.post("", **create.fastapi_endpoint_config)
def provenance_post(
    payload: ProvenancePayload,
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> JSONResponse:
    """
    Create provenance and return its ID
    """
    provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
    provenance_id: int = provenance_handler.create_entry(payload)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": provenance_id},
    )


@provenance_router.post("/search")
def search_provenance(
    payload: ProvenanceSearch,
    search_type: enums.ProvenanceSearchTypes = Query(
        default=enums.ProvenanceSearchTypes.connected_nodes
    ),
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> JSONResponse:
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
    Dataset, Model, ModelConfiguration, Publication, Simulation,
    Project, Concept.


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
                "Model",
                "ModelConfiguration",
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

    return JSONResponse(
        headers={
            "content-type": "application/json",
        },
        content={"result": results},
    )


@provenance_router.delete("/hanging_nodes")
def delete_hanging_nodes(
    rdb: Engine = Depends(request_rdb), graph_db=Depends(request_graph_db)
) -> JSONResponse:
    """
    Prunes nodes that have 0 edges
    """
    provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
    success = provenance_handler.delete_nodes()
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={
            "content-type": "application/json",
        },
        content={"success": success},
    )


@provenance_router.get(
    "/{provenance_id}",
    response_model=ProvenanceResponse,
    **retrieve.fastapi_endpoint_config,
)
def provenance_get(
    provenance_id: int, rdb: Engine = Depends(request_rdb)
) -> JSONResponse | Response:
    """
    Retrieve a provenance from ElasticSearch
    """
    try:
        with Session(rdb) as session:
            res = session.query(Provenance).get(provenance_id)

        logger.info("Provenance retrieved: %s", provenance_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(res),
        )
    except NoResultFound:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@provenance_router.delete("/{provenance_id}", **delete.fastapi_endpoint_config)
def provenance_delete(
    provenance_id: int,
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> JSONResponse:
    """
    Delete a Provenance in ElasticSearch
    """
    try:
        with Session(rdb) as session:
            if (
                session.query(Provenance).filter(Provenance.id == provenance_id).count()
                == 1
            ):
                provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
                success = provenance_handler.delete(id=provenance_id)

                success_msg = f"Provenance successfully deleted: {provenance_id}"

                logger.info(success_msg)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    headers={
                        "content-type": "application/json",
                    },
                    content={
                        "id": provenance_id,
                        "message": success_msg,
                        "success": success,
                    },
                )
            raise NoResultFound
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
            content={"message": f"Provenance record for id {provenance_id} not found"},
        )
