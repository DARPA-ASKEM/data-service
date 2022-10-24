"""
router.simulations - does nothing yet
"""

from logging import Logger
from fastapi import APIRouter
from sqlalchemy.engine.base import Engine

logger = Logger(__file__)

def gen_router(engine: Engine) -> APIRouter:
    """
    Generate simulations router with given DB engine
    """
    router = APIRouter()


    @router.get("/simulations")
    def get_sims() -> str:
        """
        Mock simulations endpoint
        """
        logger.info(engine)
        return 'SIMULATIONS NOT IMPLEMENTED!'


    return router
