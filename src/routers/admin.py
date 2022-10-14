from fastapi import APIRouter

from db import ENGINE

router = APIRouter()

@router.get('/admin/db')
def db_status() -> str:
    return 'Hello DB'



