"""
CRUD operations for concepts and related tables in the DB
"""

import json
from logging import Logger
from typing import List, Optional
from urllib.parse import quote_plus

import requests
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy import func
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import request_rdb
from tds.lib.errors import DKGError
from tds.settings import settings

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
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    base_url = settings.DKG_URL + ":" + str(settings.DKG_API_PORT)
    params = f"api/search?q={term}&limit={limit}&offset={offset}"
    url = f"{base_url}/{params}"
    logger.info("Sending data to %s", url)

    response = requests.get(url, headers=headers, timeout=5)
    logger.debug("response: %s", response)
    logger.debug("response reason: %s", response.raw.reason)

    if response.status_code == 200:
        return json.loads(response.content.decode("utf8"))
    logger.debug("Failed to fetch ontologies: %s", response)
    raise Exception(f"DKG server returned the status {response.status_code}")


@router.get("/definitions/{curie}")
def get_concept_definition(curie: str):
    """
    Wraps fetch functionality from the DKG.
    """
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    base_url = settings.DKG_URL + ":" + str(settings.DKG_API_PORT)
    params = f"api/entity/{quote_plus(curie)}"
    url = f"{base_url}/{params}"
    logger.info("Sending data to %s", url)

    response = requests.get(url, headers=headers, timeout=5)
    logger.debug("response: %s", response)
    logger.debug("response reason: %s", response.raw.reason)

    if response.status_code == 200:
        return json.loads(response.content.decode("utf8"))
    logger.debug("Failed to fetch ontologies: %s", response)
    raise DKGError("DKG server returned the status {response.status_code}")


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
                func.count(orm.OntologyConcept.curie), orm.OntologyConcept.curie
            ).group_by(orm.OntologyConcept.curie),
            "results": session.query(orm.OntologyConcept),
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

        def handle_dkg(curie):
            try:
                return get_concept_definition(curie)["name"]
            except DKGError:
                return None

        term_map = {hit[1]: handle_dkg(hit[1]) for hit in search_body["curies"]}

        return Response(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=json.dumps(
                {
                    "facets": {
                        "types": {hit[1]: hit[0] for hit in search_body["types"]},
                        "curies": {hit[1]: hit[0] for hit in search_body["curies"]},
                    },
                    "results": [
                        {
                            "type": entry.type,
                            "id": entry.object_id,
                            "curie": entry.curie,
                            "display_name": term_map[entry.curie],
                        }
                        for entry in search_body["results"]
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
        logger.info(data_payload)

        data_to_update = session.query(orm.OntologyConcept).filter(
            orm.OntologyConcept.id == id
        )
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Concept"


@router.delete("/{id}")
def delete_concept(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Delete a concept by ID
    """
    with Session(rdb) as session:
        session.query(orm.OntologyConcept).filter(orm.OntologyConcept.id == id).delete()
        session.commit()
