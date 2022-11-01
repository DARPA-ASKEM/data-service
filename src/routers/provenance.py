"""
router.provenance - does nothing yet
"""

from logging import Logger

from fastapi import APIRouter
from sqlalchemy.engine.base import Engine

logger = Logger(__file__)


def gen_router(engine: Engine, router_name: str) -> APIRouter:
    """
    Generate provenance router with given DB engine
    """
    router = APIRouter(prefix=router_name)

    @router.get("")
    def get_provenance() -> str:
        """
        Mock provenance
        """
        logger.info(engine)
        return "PROVENANCE NOT IMPLEMENTED!"

    return router
