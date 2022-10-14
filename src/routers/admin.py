from fastapi import APIRouter

from db import ENGINE
from generated.orm import Base

router = APIRouter()

@router.get('/admin/db/info')
def db_status() -> str:
    return ENGINE.name.upper()


@router.post('/admin/db/init')
def init_tables() -> str:
    Base.metadata.create_all(ENGINE)
    return "Tables initialized" 

