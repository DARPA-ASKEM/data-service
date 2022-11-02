"""
router.simulations - does nothing yet
"""

from logging import Logger

from fastapi import APIRouter

logger = Logger(__name__)
router = APIRouter()


@router.get("")
def get_sims() -> str:
    """
    Mock simulations endpoint
    """
    logger.info("SIMULATIONS ENDPOINT NOT YET CREATED")
    return "SIMULATIONS NOT IMPLEMENTED!"
