"""
CRUD operations for concepts and related tables in the DB
"""
from logging import Logger
from typing import List, Optional
from urllib.parse import quote_plus

from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import and_, func, or_
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import request_rdb
from tds.lib.concepts import fetch_from_dkg, mark_concept_active
from tds.modules.concept.model import (
    ActiveConcept,
    OntologyConcept,
    OntologyConceptPayload,
)
from tds.modules.dataset.model import Dataset
from tds.modules.model.model import Model
from tds.modules.model_configuration.model import ModelConfiguration
from tds.modules.simulation.model import Simulation

logger = Logger(__file__)
concept_router = APIRouter()


@concept_router.get("")
def search_concept(curie: str, rdb: Engine = Depends(request_rdb)):
    """
    Searches within TDS for artifacts with this concept term associated with them
    ## parameters:
            - curie: str
              example: ido:0000621
    """
    results = []
    with Session(rdb) as session:
        result_list = (
            session.query(OntologyConcept).filter(OntologyConcept.curie == curie).all()
        )

    for result in result_list:
        result.__dict__.pop("id")
        results.append(result)
    return results


@concept_router.get("/definitions")
def search_concept_definitions(term: str, limit: int = 100, offset: int = 0):
    """
    Wraps search functionality from the DKG.
    ## parameters:
        - term: str
          example: Homo sapiens
    """
    params = f"/search?q={term}&limit={limit}&offset={offset}"
    return fetch_from_dkg(params)


@concept_router.get("/definitions/{curie}")
def get_concept_definition(curie: str):
    """
    Wraps fetch functionality from the DKG.
    ## parameters:
        - curie: str
          example: ido:0000621
    """
    params = f"/entity/{quote_plus(curie)}"
    return fetch_from_dkg(params)


def get_taggable_orm(taggable_type: schema.TaggableType):
    """
    Maps resource type to ORM
    """
    enum_to_orm = {
        schema.TaggableType.features: orm.Feature,
        schema.TaggableType.qualifiers: orm.Qualifier,
        schema.TaggableType.datasets: Dataset,
        schema.TaggableType.model_configurations: ModelConfiguration,
        schema.TaggableType.models: Model,
        schema.TaggableType.projects: orm.Project,
        schema.TaggableType.publications: orm.Publication,
        schema.TaggableType.simulations: Simulation,
    }
    return enum_to_orm[taggable_type]


@concept_router.get("/facets")
def search_concept_using_facets(
    types: List[schema.TaggableType] = Query(default=list(schema.TaggableType)),
    curies: Optional[List[str]] = Query(default=None),
    is_simulation: Optional[bool] = Query(default=None),
    rdb: Engine = Depends(request_rdb),
) -> JSONResponse:
    """
    Search along type and curie facets
    """
    with Session(rdb) as session:
        base_query = session.query(OntologyConcept).filter(
            OntologyConcept.type.in_(types)
        )
        if curies is not None:
            base_query = base_query.filter(OntologyConcept.curie.in_(curies))
        if is_simulation is not None:
            base_query = base_query.join(
                Dataset,
                and_(
                    OntologyConcept.type == schema.TaggableType.datasets,
                    OntologyConcept.object_id == Dataset.id,
                ),
                isouter=True,
            ).filter(
                or_(
                    OntologyConcept.type != schema.TaggableType.datasets,
                    Dataset.simulation_run == is_simulation,
                )
            )
        result = {
            "facets": {
                "types": {  # pylint: disable=unnecessary-comprehension
                    type: count
                    for type, count in base_query.with_entities(
                        OntologyConcept.type,
                        func.count(
                            func.distinct(
                                OntologyConcept.type, OntologyConcept.object_id
                            )
                        ),
                    ).group_by(OntologyConcept.type)
                },
                "concepts": {
                    curie: {"count": count, "name": name}
                    for curie, name, count in base_query.with_entities(
                        OntologyConcept.curie,
                        ActiveConcept.name,
                        func.count(OntologyConcept.curie),
                    )
                    .join(
                        ActiveConcept,
                        OntologyConcept.curie == ActiveConcept.curie,
                        isouter=True,
                    )
                    .group_by(OntologyConcept.curie, ActiveConcept.name)
                },
            },
            "results": [
                {
                    "type": entry.type,
                    "id": entry.object_id,
                    "curie": entry.curie,
                    "name": name,
                }
                for entry, name in base_query.with_entities(
                    OntologyConcept, ActiveConcept.name
                ).join(
                    ActiveConcept,
                    OntologyConcept.curie == ActiveConcept.curie,
                )
            ],
        }
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=result,
        )


@concept_router.get("/{concept_id}")
def get_concept(
    concept_id: int, rdb: Engine = Depends(request_rdb)
) -> Response | JSONResponse:
    """
    Get a specific concept by ID
    ## Parameters:
        - concept_id: int
    """
    with Session(rdb) as session:
        result = session.query(OntologyConcept).get(concept_id)
        if result is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(result),
        )


@concept_router.post("")
def create_concept(
    payload: OntologyConceptPayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Create a concept
    ## Example post body:
        {
            "curie": "ido:0000621",
            "type": "models",
            "object_id": "model_id",
            "status": "obj"
        }
    """
    with Session(rdb) as session:
        concept_dict = payload.dict()
        concept = OntologyConcept(**concept_dict)
        mark_concept_active(session, concept.curie)
        session.add(concept)
        session.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            headers={
                "content-type": "application/json",
            },
            content={"id": concept.id},
        )


@concept_router.put("/{concept_id}")
def update_concept(
    payload: OntologyConceptPayload, concept_id: int, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Update a concept by ID
    ## Example put body:
        {
            "curie": "ido:0000621",
            "type": "models",
            "object_id": "new_model_id",
            "status": "obj"
        }
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = concept_id
        mark_concept_active(session, data_payload["curie"])
        logger.info(data_payload)

        data_to_update = session.query(OntologyConcept).filter(
            OntologyConcept.id == concept_id
        )
        data_to_update.update(data_payload)
        session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        headers={
            "content-type": "application/json",
        },
        content={"message": "Updated Concept"},
    )


@concept_router.delete("/{concept_id}")
def delete_concept(concept_id: int, rdb: Engine = Depends(request_rdb)):
    """
    Delete a concept by ID
    """
    with Session(rdb) as session:
        session.query(OntologyConcept).filter(OntologyConcept.id == concept_id).delete()
        session.commit()
