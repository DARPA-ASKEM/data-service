"""
Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from typing import Dict, List, Optional, Set

from tds.db.enums import ResourceType
from tds.modules.project.model import Project as ProjectModel
from tds.modules.project.model import ProjectAsset, ProjectPayload
from tds.schema.concept import Concept


class Project(ProjectPayload):
    concept: Optional[Concept] = None
    active = True
    assets: Dict[ResourceType, Set[int | str]] = {}

    @classmethod
    def from_orm(
        cls, body: ProjectModel, project_assets: List[ProjectAsset]
    ) -> "Project":
        """
        Handle the creation of asset dict
        """
        assets = {type: [] for type in ResourceType}
        for asset in project_assets:
            assets[asset.resource_type].append(asset.resource_id)

        body.__dict__["assets"] = assets
        return super().from_orm(body)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "string",
                "description": "string",
                "assets": {"resource-type": "list-of-ordered-ints"},
                "active": "bool",
            }
        }


class ProjectMetadata(ProjectPayload):
    concept: Optional[Concept] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "string",
                "description": "string",
                "active": True,
            }
        }
