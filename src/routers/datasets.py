"""
router.datasets - doesn't do much yet
"""
from logging import Logger
from fastapi import APIRouter
from sqlalchemy.orm import Session
from generated import  orm
from config.db import engine
import config.schema

logger = Logger(__file__)
router = APIRouter()

@router.post('/datasets')
def create_dataset(payload : config.schema.Dataset ) -> str:
    """
    Create dataset naively
    """
    with Session(engine) as session:
        datasetp = payload.dict()
        del datasetp['id']
        dataset = orm.Dataset(**datasetp)
        session.add(dataset)
        session.commit()
        for feature_payload in payload.features:
            feature_dict = feature_payload.dict()
            del feature_dict['id']
            feature_dict['dataset_id'] = dataset.id
            feature = orm.Feature(**feature_dict)
            session.add(feature)
        session.commit()
    return 'Created dataset'
