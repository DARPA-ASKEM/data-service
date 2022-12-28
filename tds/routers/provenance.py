"""

router.provenance - very basic crud operations for provenance

"""

import json
from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db import ProvenanceHandler, request_graph_db, request_rdb
from tds.operation import create, delete, retrieve
from tds.schema.provenance import Provenance

logger = Logger(__name__)
router = APIRouter()


@router.get("", **retrieve.fastapi_endpoint_config)
def get_provenance(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Searches within TDS for artifacts with this concept term associated with them
    """
    with Session(rdb) as session:
        return Provenance.from_orm(session.query(orm.Provenance).get(id))


@router.get("/derived_from")
def search_provenance(
    artifact_id: int,
    artifact_type: str,
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> Response:
    """
    Search provenance of for all artifacts that helped derive this artifact.
    """
    logger.info("search provenance")
    provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
    list_of_artifacts = provenance_handler.search_derivedfrom(
        artifact_id=artifact_id, artifact_type=artifact_type
    )
    return Response(
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"provenance": list_of_artifacts}),
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
    print(rdb)
    print(graph_db)
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
