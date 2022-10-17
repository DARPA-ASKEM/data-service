"""
router.admin - Wraps administrative functions for interacting with the DB.
"""

from fastapi import APIRouter

from db import ENGINE
from generated.orm import Base

router = APIRouter()


@router.get('/admin/db/info')
def db_status() -> str:
    """
    Print kind of DB being used
    """
    return ENGINE.name.upper()


@router.post('/admin/db/init')
def init_tables() -> str:
    """
    Initialize tables in the connected DB
    """
    Base.metadata.create_all(ENGINE)
    return "Tables initialized" 

