"""
TDS Provenance Response object.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from tds.autogen.enums import ProvenanceType, RelationType


class ProvenanceResponse(BaseModel):
    """
    Provenance Response Object.
    """

    id: str
    relation_type: RelationType
    left: str
    left_type: ProvenanceType
    right: str
    right_type: ProvenanceType
    user_id: Optional[int]
    concept: str
    timestamp: datetime


def provenance_response(provenance_list):
    """
    Function builds list of provenances for response.
    """
    return [ProvenanceResponse(**x["_source"]) for x in provenance_list]
