"""
router.concepts - does nothing yet.
"""

from logging import Logger

from fastapi import APIRouter
from sqlalchemy.engine.base import Engine

logger = Logger(__file__)


def gen_router(engine: Engine) -> APIRouter:
    """
    Generate concepts router with given DB engine
    """
    router = APIRouter()

    @router.get("/concepts")
    def get_concepts() -> str:
        """
        Mock concept endpoint
        """
        logger.info(engine)
        return "CONCEPTS NOT IMPLEMENTED!"

    return router
