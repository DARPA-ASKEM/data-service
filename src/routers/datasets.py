"""
router.datasets - doesn't do much yet
"""
from fastapi import APIRouter
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from generated import  orm
import config.schema


def gen_router(engine: Engine) -> APIRouter:
    """
    Generate software router with given DB engine
    """

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

    return router
