"""
router.datasets - does nothing yet 
"""

from fastapi import APIRouter

router = APIRouter()

@router.get('/datasets')
def get_datasets() -> str:
    return 'No data'

