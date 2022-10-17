"""
router.simulations - does nothing yet
"""

from fastapi import APIRouter

router = APIRouter()

@router.get('/simulations')
def get_simulations() -> str:
    return 'No simulations'
