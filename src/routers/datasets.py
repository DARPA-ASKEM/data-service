"""
router.datasets - does nothing yet 
"""

from db import ENGINE
from pydantic import BaseModel
from fastapi import APIRouter
from generated import schema, orm
from logging import Logger
from sqlalchemy.orm import Session
from typing import List

logger = Logger(__file__)
router = APIRouter()

@router.get('/datasets')
def get_datasets() -> str:
    return 'No data'

class CreateDatasetRequest(BaseModel):
    dataset : schema.Datasets
    features : List[schema.Features]

@router.post('/datasets')
def create_dataset(payload : CreateDatasetRequest ) -> str:
    with Session(ENGINE) as session:
        datasetp = payload.dataset.dict()
        del datasetp['id']
        dataset = orm.Datasets(**datasetp)
        session.add(dataset)
        session.commit()
        for f in payload.features:
            feat = f.dict()
            del feat['id']
            feat['dataset_id'] = dataset.id
            feature = orm.Features(**feat)
            session.add(feature)
        session.commit()
    return 'Created dataset'
