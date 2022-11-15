"""
Does nothing yet
"""

from logging import Logger

from fastapi import APIRouter

logger = Logger(__name__)
router = APIRouter()


@router.get("")
def get_provenance() -> str:
    """
    Mock provenance
    """
    logger.info("PROVENANCE ENDPOINT NOT YET CREATED")
    return "PROVENANCE NOT IMPLEMENTED!"
