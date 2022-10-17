"""
router.concepts - does nothing yet.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get('/concepts')
def get_concepts() -> str:
    return 'No concepts'
