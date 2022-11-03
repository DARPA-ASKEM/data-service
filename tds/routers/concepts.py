"""
router.concepts - does nothing yet.
"""

from logging import Logger

from fastapi import APIRouter

logger = Logger(__name__)
router = APIRouter()


@router.get("")
def get_concepts() -> str:
    """
    Mock concept endpoint
    """
    logger.info("CONCEPTS ENDPOINT NOT YET CREATED")
    return "CONCEPTS NOT IMPLEMENTED!"
