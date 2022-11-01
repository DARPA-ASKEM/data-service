"""
router.admin - Wraps administrative functions for interacting with the DB.
"""

from fastapi import APIRouter
from sqlalchemy.engine.base import Engine


def gen_router(engine: Engine, router_name: str) -> APIRouter:
    """
    Generate admin router with given DB engine
    """
    router = APIRouter(prefix=router_name)

    @router.get("/db/info")
    def db_status() -> str:
        """
        Print kind of DB being used
        """
        return engine.name.upper()

    return router
