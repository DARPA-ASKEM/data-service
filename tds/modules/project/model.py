"""
TDS Project Data Model Definition.
"""
from typing import Optional

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from tds.db.base import Base
from tds.db.enums import ResourceType


class Project(Base):
    """
    Project data model.
    """

    __tablename__ = "project"

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), server_default=func.now())
    active = sa.Column(sa.Boolean(), nullable=False)
    username = sa.Column(sa.String())

    assets = relationship(
        "ProjectAsset",
        uselist=True,
        foreign_keys=[id],
        primaryjoin="Project.id == ProjectAsset.project_id",
    )

    class Config:
        """
        Project Data Model Swagger Example
        """

        schema_extra = {"example": {}}


class ProjectPayload(BaseModel):
    """
    Project Pydantic Model.
    """

    id: Optional[int] = None
    name: str
    description: str
    assets: Optional[dict]
    active: bool
    username: Optional[str]

    class Config:
        """
        Project Data Model Swagger Example
        """

        schema_extra = {
            "example": {
                "name": "A cool project",
                "description": "Project info goes here.",
                "assets": [],
                "active": "true",
                "username": "Loki",
            }
        }


class ProjectAsset(Base):
    """
    ProjectAsset Data Model.
    """

    __tablename__ = "project_asset"

    id = sa.Column(sa.Integer(), primary_key=True)
    project_id = sa.Column(sa.Integer(), sa.ForeignKey("project.id"), nullable=False)
    resource_id = sa.Column(sa.String(), nullable=False)
    resource_type = sa.Column(sa.Enum(ResourceType), nullable=False)
    external_ref = sa.Column(sa.String())


class ProjectAssetPayload(BaseModel):
    """
    ProjectAssetPayload Data Model.
    """

    id: Optional[int] = None
    project_id: Optional[int] = None
    resource_id: Optional[int] = None
    resource_type: ResourceType
    external_ref: Optional[str]
