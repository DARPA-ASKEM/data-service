"""
CRUD operations for datasets and related tables in the DB
"""

import json
from logging import DEBUG, Logger
from typing import List

import requests
from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import StreamingResponse
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import request_rdb
from tds.lib.datasets import create_qualifier_xref

logger = Logger(__file__)
logger.setLevel(DEBUG)
router = APIRouter()


@router.get("")
def get_datasets(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a specific number of datasets
    """
    with Session(rdb) as session:
        return list(
            session.query(orm.Dataset)
            .order_by(orm.Dataset.timestamp.asc())
            .limit(count)
        )


@router.get("/{id}")
def get_dataset(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific dataset by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Dataset).get(id)
        return result


@router.post("")
def create_dataset(payload: schema.Dataset, rdb: Engine = Depends(request_rdb)):
    """
    Create a dataset
    """
    with Session(rdb) as session:
        datasetp = payload.dict()
        del datasetp["id"]
        dataset = orm.Dataset(**datasetp)
        session.add(dataset)
        session.commit()
        logger.debug(dataset)
        data_id = dataset.id
        datasetp["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/datasets/{data_id}",
                "content-type": "application/json",
            },
            content=json.dumps(datasetp, default=str),
        )


@router.patch("/{id}")
def update_dataset(
    payload: schema.Dataset, id: int, rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Update a dataset by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(
            exclude_unset=True
        )  # Exclude unset not working, throws 422 if schema.Datasets is malformed.
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Dataset).filter(orm.Dataset.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "location": f"/api/datasets/{id}",
            "content-type": "application/json",
        },
        content=json.dumps(data_to_update, default=str),
    )


@router.post("/deprecate/{id}")
def deprecate_dataset(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Toggle a dataset's deprecated status by ID
    """
    with Session(rdb) as session:
        to_toggle_deprecated = session.query(orm.Dataset).filter(orm.Dataset.id == id)
        deprecated_value = not to_toggle_deprecated.first().deprecated
        to_toggle_deprecated.update({"deprecated": deprecated_value})
        session.commit()
        return f"Set dataset with id {id} to deprecated state {deprecated_value}"


# Not working because of lack of cascade settings in ORM?
# Features foreign key blocks the delete.
@router.delete("/{id}")
def delete_dataset(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Delete a dataset by ID
    """
    with Session(rdb) as session:
        session.query(orm.Dataset).filter(orm.Dataset.id == id).delete()
        session.commit()


@router.get("/{id}/download/csv")
def get_csv(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Gets the csv of an annotated dataset that is registered
    via the data-annotation tool.
    """
    dataset = get_dataset(id=id, rdb=rdb)
    data_paths = dataset.annotations["data_paths"]

    response = requests.post(
        "http://data-annotation-api:80/datasets/download/csv",
        params={"data_path_list": data_paths},
        stream=True,
        timeout=15,
    )

    return StreamingResponse(response.raw, headers=response.headers)


@router.get("/features")
def get_features(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a specified number of features
    """
    with Session(rdb) as session:
        result = session.query(orm.Feature).order_by(orm.Feature.id.asc()).limit(count)
        result = result[::]
        return result


@router.get("/features/{id}")
def get_feature(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific feature by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Feature).get(id)
        return result


@router.post("/features")
def create_feature(payload: schema.Feature, rdb: Engine = Depends(request_rdb)):
    """
    Create a feature
    """
    with Session(rdb) as session:
        featurep = payload.dict()
        del featurep["id"]
        feature = orm.Feature(**featurep)
        exists = session.query(orm.Feature).filter_by(**featurep).first() is not None
        if exists:
            return Response(
                status_code=status.HTTP_200_OK,
                headers={
                    "location": "/api/features/",
                    "content-type": "application/json",
                },
                content=json.dumps(featurep),
            )
        session.add(feature)
        session.commit()
        data_id = feature.id
        featurep["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/features/{data_id}",
                "content-type": "application/json",
            },
            content=json.dumps(featurep),
        )


@router.patch("/features/{id}")
def update_feature(
    payload: schema.Feature, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Update a feature by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Feature).filter(orm.Feature.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Feature"


@router.delete("/features/{id}")
def delete_feature(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Delete a feature by ID
    """
    with Session(rdb) as session:
        session.query(orm.Feature).filter(orm.Feature.id == id).delete()
        session.commit()


@router.get("")
def get_qualifiers(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a specific number of qualifiers
    """
    with Session(rdb) as session:
        return list(
            session.query(orm.Qualifier).order_by(orm.Qualifier.id.asc()).limit(count)
        )


@router.get("/qualfiers/{id}")
def get_qualifier(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific qualifier by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Qualifier).get(id)
        return result


@router.post("/qualfiers")
def create_qualifier(
    payload: schema.Qualifier,
    qualifies_array: List[str],
    rdb: Engine = Depends(request_rdb),
):
    """
    Create a qualifier
    """
    with Session(rdb) as session:
        qualifierp = payload.dict()
        del qualifierp["id"]
        qualifier = orm.Qualifier(**qualifierp)
        exists = (
            session.query(orm.Qualifier).filter_by(**qualifierp).first() is not None
        )
        if exists:
            return Response(
                status_code=status.HTTP_200_OK,
                headers={
                    "location": "/api/qualfiers/",
                    "content-type": "application/json",
                },
                content=json.dumps(qualifierp),
            )

        session.add(qualifier)
        session.commit()
        data_id = qualifier.id
        for qual in qualifies_array:
            feature = (
                session.query(orm.Feature)
                .filter_by(name=qual, dataset_id=qualifierp["dataset_id"])
                .first()
            )
            qualifier_xrefp = {
                "id": 0,
                "qualifier_id": data_id,
                "feature_id": feature.id,
            }
            create_qualifier_xref(qualifier_xrefp, rdb)
        qualifierp["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/qualifiers/{data_id}",
                "content-type": "application/json",
            },
            content=json.dumps(qualifierp),
        )


@router.patch("/qualfiers/{id}")
def update_qualifier(
    payload: schema.Qualifier, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Update a qualifier by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Qualifier).filter(orm.Qualifier.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Qualifier"


@router.delete("/qualfiers/{id}")
def delete_qualifier(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Delete a qualifier by ID
    """
    with Session(rdb) as session:
        session.query(orm.Qualifier).filter(orm.Qualifier.id == id).delete()
        session.commit()
