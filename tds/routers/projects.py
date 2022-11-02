"""
router.projects - does nothing yet
"""

from logging import Logger

from fastapi import APIRouter

logger = Logger(__name__)
router = APIRouter()


@router.get("")
def get_projects() -> str:
    """
    Mock project endpoint
    """
    logger.info("PROJECTS ENDPOINT NOT YET CREATED")
    return "PROJECTS NOT IMPLEMENTED!"
