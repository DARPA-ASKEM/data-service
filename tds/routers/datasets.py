"""
router.datasets - doesn't do much yet
"""

from logging import Logger

from fastapi import APIRouter, Depends
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db import request_rdb
from tds.operation import create
from tds.schema.dataset import Dataset

logger = Logger(__name__)
router = APIRouter()


@router.post("", **create.fastapi_endpoint_config)
def create_dataset(payload: Dataset, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Create dataset naively
    """
    with Session(rdb) as session:
        datasetp = payload.dict()
        del datasetp["id"]
        dataset = orm.Dataset(**datasetp)
        session.add(dataset)
        session.commit()
        for feature_payload in payload.features:
            feature_dict = feature_payload.dict()
            del feature_dict["id"]
            feature_dict["dataset_id"] = dataset.id
            feature = orm.Feature(**feature_dict)
            session.add(feature)
        session.commit()

    logger.info("new dataset created")
    return "Created dataset"
