"""
router.admin - Wraps administrative functions for interacting with the DB.
"""

from fastapi import APIRouter

from db import ENGINE
from generated import orm
from sqlalchemy.orm import Session

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
    orm.Base.metadata.create_all(ENGINE)
    return "Tables initialized"


@router.post('/admin/framework/init')
def init_catlab_data() -> str:
    """
    Initialize dummy frameworks
    """
    with Session(ENGINE) as session:
        framework = orm.Framework(
            id = 0,
            version = "dummy",
            name = "dummy",
            semantics = {},
        )
        session.add(framework)
        session.commit()
    return "Dummy framework created"

