"""
router.datasets - doesn't do much yet
"""
from fastapi import APIRouter
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from src.autogen import orm
from src.operation import create
from src.schema.dataset import Dataset


def gen_router(engine: Engine, router_name: str) -> APIRouter:
    """
    Generate software router with given DB engine
    """

    router = APIRouter(prefix=router_name)

    @router.post("", **create.fastapi_endpoint_config)
    def create_dataset(payload: Dataset) -> str:
        """
        Create dataset naively
        """
        with Session(engine) as session:
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
        return "Created dataset"

    return router
