"""
router.projects - does nothing yet
"""

from logging import Logger
from fastapi import APIRouter
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from generated import schema, orm

logger = Logger(__file__)


def gen_router(engine: Engine) -> APIRouter:
    """
    Generate projecs router with given DB engine
    """
    router = APIRouter()


    @router.get("/projects")
    def get_projects() -> str:
        """
        Mock project endpoint
        """
        logger.info(engine)
        return 'PROJECTS NOT IMPLEMENTED!'


    return router
