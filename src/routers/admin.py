"""
router.admin - Wraps administrative functions for interacting with the DB.
"""

from fastapi import APIRouter
from db import ENGINE

router = APIRouter()


@router.get('/admin/db/info')
def db_status() -> str:
    """
    Print kind of DB being used
    """
    return ENGINE.name.upper()


