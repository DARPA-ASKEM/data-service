from fastapi import APIRouter

router = APIRouter()

@router.get('/admin/db')
def db_status() -> str:
    return 'Hello DB'



