"""
router.datasets - crud operations for datasets and related tables in the DB
"""

import json
from db import ENGINE
from pydantic import BaseModel
from fastapi import APIRouter
from generated import schema, orm
import api_schema
from logging import Logger
from sqlalchemy.orm import Session
from typing import List

logger = Logger(__file__)
router = APIRouter()


@router.get("/datasets")
def get_datasets(count: int) -> str:
    with Session(ENGINE) as session:
        result = session.query(orm.Dataset).order_by(orm.Dataset.id.desc()).limit(count)
        logger.info(f"Pre manip result: {result}")
        result = result[::-1]
        logger.info(f"Latest output: {result}")
        return result


@router.get("/datasets/{id}")
def get_datasets(id: int) -> str:
    with Session(ENGINE) as session:
        result = session.query(orm.Dataset).get(id)
        logger.info(f"Latest output: {result}")
        return result


@router.post("/datasets")
def create_dataset(payload: api_schema.Dataset) -> str:
    with Session(ENGINE) as session:
        datasetp = payload.dict()
        del datasetp["id"]
        dataset = orm.Dataset(**datasetp)
        session.add(dataset)
        session.commit()
        for f in payload.features:
            feat = f.dict()
            del feat["id"]
            feat["dataset_id"] = dataset.id
            feature = orm.Feature(**feat)
            session.add(feature)
        session.commit()
    return "Created dataset"


@router.patch("/datasets/{id}")
def update_dataset(payload: schema.Dataset, id: int) -> str:
    with Session(ENGINE) as session:
        data_payload = payload.dict(
            exclude_unset=True
        )  # Exclude unset not working, throws 422 if schema.Datasets in malformed.
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Dataset).filter(orm.Dataset.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated dataset"


@router.post("/datasets/deprecate/{id}")
def deprecate_dataset(id: int) -> str:
    with Session(ENGINE) as session:
        to_toggle_deprecated = session.query(orm.Dataset).filter(orm.Dataset.id == id)
        deprecated_value = not to_toggle_deprecated.first().deprecated
        to_toggle_deprecated.update({"deprecated": deprecated_value})
        session.commit()
        return f"Set dataset with id {id} to deprecated state {deprecated_value}"


# Not working because of lack of cascade settings in ORM? Features foreign key blocks the delete.
@router.delete("/datasets/{id}")
def delete_dataset(id: int) -> str:
    with Session(ENGINE) as session:
        session.query(orm.Dataset).filter(orm.Dataset.id == id).delete()
        session.commit()
