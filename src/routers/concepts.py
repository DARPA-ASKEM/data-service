"""
router.concepts - does nothing yet.
"""

from logging import Logger

from fastapi import APIRouter
from sqlalchemy.engine.base import Engine


def gen_router(engine: Engine, router_name: str) -> APIRouter:
    """
    Generate concepts router with given DB engine
    """
    logger = Logger(router_name)
    router = APIRouter(prefix=router_name)

    @router.get("")
    def get_concepts() -> str:
        """
        Mock concept endpoint
        """
        logger.info(engine)
        return "CONCEPTS NOT IMPLEMENTED!"

    return router
