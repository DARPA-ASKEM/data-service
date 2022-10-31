"""
router.admin - Wraps administrative functions for interacting with the DB.
"""

from fastapi import APIRouter
from sqlalchemy.engine.base import Engine


def gen_router(engine: Engine) -> APIRouter:
    """
    Generate admin router with given DB engine
    """
    router = APIRouter()

    @router.get("/admin/db/info")
    def db_status() -> str:
        """
        Print kind of DB being used
        """
        return engine.name.upper()

    return router
