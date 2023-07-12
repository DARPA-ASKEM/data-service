"""
TDS Concept Data Model.
"""
from typing import Optional

import sqlalchemy as sa
from pydantic import BaseModel

from tds.db import Base
from tds.db.enums import OntologicalField, TaggableType


class OntologyConcept(Base):
    """
    OntologyConcept Data Model.
    """

    __tablename__ = "ontology_concept"

    id = sa.Column(sa.Integer(), primary_key=True)
    curie = sa.Column(
        sa.String(), sa.ForeignKey("active_concept.curie"), nullable=False
    )
    type = sa.Column(sa.Enum(TaggableType), nullable=False)
    object_id = sa.Column(sa.String(), nullable=False)
    status = sa.Column(sa.Enum(OntologicalField), nullable=False)


class ActiveConcept(Base):
    """
    ActiveConcept Data Model.
    """

    __tablename__ = "active_concept"

    curie = sa.Column(sa.String(), primary_key=True)
    name = sa.Column(sa.String())


class OntologyConceptPayload(BaseModel):
    """
    OntologyConcept Pydantic Model.
    """

    id: Optional[int] = None
    curie: str
    type: TaggableType
    object_id: str
    status: OntologicalField
