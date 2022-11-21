"""

router.provenance - very basic crud operations for provenance

"""

import json
from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db import request_graph_engine, request_rdb
from tds.db.graph import ProvenanceHandler
from tds.operation import create, delete, retrieve
from tds.schema.provenance import Provenance

logger = Logger(__name__)
router = APIRouter()


@router.get("")
def get_provenance(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Searches within TDS for artifacts with this concept term associated with them
    """
    with Session(rdb) as session:
        results = session.query(orm.Provenance).filter(orm.Provenance.id == id).all()

    return results


@router.get("/derived_from")
def search_provenance(
    artifact_id: int,
    artifact_type: str,
    rdb: Engine = Depends(request_rdb),
    neo_engine=Depends(request_graph_engine),
) -> list:
    """
    Search provenance of for all artifacts that helped derive this artifact.
    """
    logger.info("search provenance")
    provenance_handler = ProvenanceHandler(rdb=rdb, neo_engine=neo_engine)
    list_of_artifacts = provenance_handler.search_derivedfrom(
        artifact_id=artifact_id, artifact_type=artifact_type
    )
    print(list_of_artifacts)
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
    neo_engine=Depends(request_graph_engine),
) -> dict:
    """
    Create provenance relationship
    """
    provenance_handler = ProvenanceHandler(rdb=rdb, neo_engine=neo_engine)
    provenance_payload = payload.dict()
    id: int = provenance_handler.create(
        left=provenance_payload.get("left"),
        left_type=provenance_payload.get("left_type"),
        right=provenance_payload.get("right"),
        right_type=provenance_payload.get("right_type"),
        relation_type=provenance_payload.get("relation_type"),
        user_id=provenance_payload.get("user_id"),
    )

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
    rdb: Engine = Depends(request_rdb), neo_engine=Depends(request_graph_engine)
) -> Response:
    print("here")
    provenance_handler = ProvenanceHandler(rdb=rdb, neo_engine=neo_engine)
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
    neo_engine=Depends(request_graph_engine),
) -> Response:
    """
    Delete provenance metadata
    """
    with Session(rdb) as session:
        if session.query(orm.Provenance).filter(orm.Provenance.id == id).count() == 1:

            provenance_handler = ProvenanceHandler(rdb=rdb, neo_engine=neo_engine)
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
