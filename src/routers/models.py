"""
router.models - does nothing yet
"""

from fastapi import APIRouter

router = APIRouter()

@router.get('/models')
def get_models() -> str:
    return 'No models'
