"""
router.provenance - does nothing yet
"""

from fastapi import APIRouter

router = APIRouter()

@router.get('/provenance')
def get_datasets() -> str:
    return 'No provenance'
