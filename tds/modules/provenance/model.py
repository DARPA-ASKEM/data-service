"""
TDS Provenance Data Model Definition.
"""
import datetime
from typing import List, Optional

import sqlalchemy as sa
from pydantic import Field
from pydantic.main import BaseModel
from sqlalchemy import func

from tds.autogen.orm import Base
from tds.db.enums import ProvenanceType, RelationType


class Provenance(Base):
    """
    Provenance Data Model
    """

    __tablename__ = "provenance"

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    relation_type = sa.Column(sa.Enum(RelationType), nullable=False)
    left = sa.Column(sa.String(), nullable=False)
    left_type = sa.Column(sa.Enum(ProvenanceType), nullable=False)
    right = sa.Column(sa.String(), nullable=False)
    right_type = sa.Column(sa.Enum(ProvenanceType), nullable=False)
    user_id = sa.Column(sa.Integer(), sa.ForeignKey("person.id"))
    concept = sa.Column(sa.String())

    class Config:
        """
        Provenance Data Model Swagger Example
        """

        schema_extra = {"example": {}}


class ProvenancePayload(BaseModel):
    """
    Provenance Payload Data Model
    """

    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    relation_type: RelationType
    left: str
    left_type: ProvenanceType
    right: str
    right_type: ProvenanceType
    user_id: Optional[int]
    concept: Optional[str]


class ProvenanceSearch(BaseModel):
    """
    Provenance Data Model.
    """

    root_id: Optional[int]
    root_type: Optional[ProvenanceType]
    user_id: Optional[int]
    curie: Optional[str]
    edges: Optional[bool]
    nodes: Optional[bool]
    types: List[ProvenanceType] = Field(
        default=[
            type
            for type in ProvenanceType
            if type not in ["Concept", "ModelRevision", "Project"]
        ]
    )
    hops: Optional[int]
    limit: Optional[int]
    verbose: Optional[bool]
