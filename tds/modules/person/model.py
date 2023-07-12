"""
TDS Person Data Model Definition.
"""
from typing import Any, List, Optional

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.orm import relationship

from tds.autogen.orm import Base
from tds.db.enums import ResourceType, Role


class Person(Base):
    """
    Person Data Model
    """

    __tablename__ = "person"

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    email = sa.Column(sa.String(), nullable=False)
    org = sa.Column(sa.String())
    website = sa.Column(sa.String())
    is_registered = sa.Column(sa.Boolean(), nullable=False)

    associations = relationship(
        "Association",
        uselist=True,
        foreign_keys=[id],
        primaryjoin="Person.id == Association.person_id",
        backref="person",
        cascade_backrefs=False,
        # cascade="save-update",
        # single_parent=True,
    )

    class Config:
        """
        Person Data Model Swagger Example
        """

        schema_extra = {"example": {}}


class PersonPayload(BaseModel):
    """
    PersonPayload Data Model.
    """

    id: Optional[int] = None
    name: str
    email: str
    org: Optional[str]
    website: Optional[str]
    is_registered: bool


class Association(Base):
    """
    Association Data Model
    """

    __tablename__ = "association"

    id = sa.Column(sa.Integer(), primary_key=True)
    person_id = sa.Column(sa.Integer(), sa.ForeignKey("person.id"), nullable=False)
    resource_id = sa.Column(sa.String(), nullable=False)
    resource_type = sa.Column(sa.Enum(ResourceType))
    role = sa.Column(sa.Enum(Role))

    person = relationship("Person", cascade=False, single_parent=True)


class AssociationPayload(BaseModel):
    """
    PersonPayload Data Model.
    """

    id: Optional[int] = None
    person_id: int
    resource_id: str
    resource_type: ResourceType
    role: Role
