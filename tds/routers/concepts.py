"""
CRUD operations for concepts and related tables in the DB
"""

import json
from logging import Logger
from urllib.parse import quote_plus

import requests
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import request_rdb
from tds.settings import settings

logger = Logger(__file__)
router = APIRouter()


@router.get("")
<<<<<<< HEAD
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
=======
def search_concept(term: str, limit: int = 100, offset: int = 0):
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


@router.get("/definition/{curie}")
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
    raise Exception("DKG server returned the status {response.status_code}")
>>>>>>> 219f907 (Bump to `v0.3.0` (#50))

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
    raise Exception("DKG server returned the status {response.status_code}")


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
