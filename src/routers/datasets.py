"""
router.datasets - does nothing yet 
"""

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

@router.get('/datasets')
def get_datasets() -> str:
    return 'No data'

@router.post('/datasets')
def create_dataset(payload : api_schema.Dataset ) -> str:
    with Session(ENGINE) as session:
        datasetp = payload.dict()
        del datasetp['id']
        dataset = orm.Dataset(**datasetp)
        session.add(dataset)
        session.commit()
        for f in payload.features:
            feat = f.dict()
            del feat['id']
            feat['dataset_id'] = dataset.id
            feature = orm.Feature(**feat)
            session.add(feature)
        session.commit()
    return 'Created dataset'
