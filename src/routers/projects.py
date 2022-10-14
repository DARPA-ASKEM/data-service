from fastapi import APIRouter

router = APIRouter()

@router.get('/projects')
def list_all_projects() -> str:
    return 'Will eventually return list of all projects??'

