"""
CRUD operations for concepts and related tables in the DB
"""

import json
from logging import Logger
from typing import List, Optional
from urllib.parse import quote_plus

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy import func
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import request_rdb
from tds.lib.concepts import fetch_from_dkg, mark_concept_active

logger = Logger(__file__)
router = APIRouter()


@router.get("")
def search_concept(curie: str, rdb: Engine = Depends(request_rdb)):
    """
    Searches within TDS for artifacts with this concept term associated with them
    """
    results = []
    with Session(rdb) as session:
        result_list = (
            session.query(orm.OntologyConcept)
            .filter(orm.OntologyConcept.curie == curie)
            .all()
        )

    for result in result_list:
        result.__dict__.pop("id")
        results.append(result)
    return results


@router.get("/definitions")
def search_concept_definitions(term: str, limit: int = 100, offset: int = 0):
    """
    Wraps search functionality from the DKG.
    """
    params = f"/search?q={term}&limit={limit}&offset={offset}"
    return fetch_from_dkg(params)


@router.get("/definitions/{curie}")
def get_concept_definition(curie: str):
    """
    Wraps fetch functionality from the DKG.
    """
    params = f"/entity/{quote_plus(curie)}"
    return fetch_from_dkg(params)


@router.get("/facets")
def search_concept_using_facets(
    types: List[schema.TaggableType] = Query(default=None),
    curies: Optional[List[str]] = Query(default=None),
    rdb: Engine = Depends(request_rdb),
) -> Response:
    """
    Search along type and curie facets
    """
    with Session(rdb) as session:
        search_body = {
            "types": session.query(
                func.count(orm.OntologyConcept.type), orm.OntologyConcept.type
            ).group_by(orm.OntologyConcept.type),
            "curies": session.query(
                func.count(orm.OntologyConcept.curie),
                orm.OntologyConcept.curie,
                orm.ActiveConcept.name,
            )
            .join(
                orm.ActiveConcept,
                orm.OntologyConcept.curie == orm.ActiveConcept.curie,
                isouter=True,
            )
            .group_by(orm.OntologyConcept.curie, orm.ActiveConcept.name),
            "results": session.query(orm.OntologyConcept, orm.ActiveConcept.name).join(
                orm.ActiveConcept,
                orm.OntologyConcept.curie == orm.ActiveConcept.curie,
                isouter=True,
            ),
        }
        for key in search_body:
            if types is not None:
                search_body[key] = search_body[key].filter(
                    orm.OntologyConcept.type.in_(types)
                )
            if curies is not None:
                search_body[key] = search_body[key].filter(
                    orm.OntologyConcept.curie.in_(curies)
                )

        return Response(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=json.dumps(
                {
                    "facets": {
                        "types": {hit[1]: hit[0] for hit in search_body["types"]},
                        "concepts": {
                            hit[1]: {"count": hit[0], "name": hit[2]}
                            for hit in search_body["curies"]
                        },
                    },
                    "results": [
                        {
                            "type": entry.type,
                            "id": entry.object_id,
                            "curie": entry.curie,
                            "name": name,
                        }
                        for entry, name in search_body["results"]
                    ],
                }
            ),
        )


@router.get("/{id}")
def get_concept(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific concept by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.OntologyConcept).get(id)
        return result


@router.post("")
def create_concept(payload: schema.OntologyConcept, rdb: Engine = Depends(request_rdb)):
    """
    Create a concept
    """
    with Session(rdb) as session:
        concept_dict = payload.dict()
        concept = orm.OntologyConcept(**concept_dict)
        mark_concept_active(session, concept.curie)
        session.add(concept)
        session.commit()
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "content-type": "application/json",
            },
            content=json.dumps({"id": concept.id}),
        )


@router.patch("/{id}")
def update_concept(
    payload: schema.OntologyConcept, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Update a concept by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        mark_concept_active(session, data_payload["curie"])
        logger.info(data_payload)

        data_to_update = session.query(orm.OntologyConcept).filter(
            orm.OntologyConcept.id == id
        )
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Concept"


@router.delete("/{id}")
def delete_concept(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Delete a concept by ID
    """
    with Session(rdb) as session:
        session.query(orm.OntologyConcept).filter(orm.OntologyConcept.id == id).delete()
        session.commit()
