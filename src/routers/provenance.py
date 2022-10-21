"""
router.provenance - does nothing yet
"""

from fastapi import APIRouter

router = APIRouter()

@router.get('/provenance')
def get_provenance_relations() -> str:
    return 'No provenance'
