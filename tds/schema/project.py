"""
Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from typing import Dict, List, Optional, Set

from tds.autogen import orm, schema
from tds.schema.concept import Concept


class Project(schema.Project):
    concept: Optional[Concept] = None
    active = True
    assets: Dict[schema.ResourceType, Set[int]] = {}

    @classmethod
    def from_orm(
        cls, body: orm.Project, project_assets: List[orm.ProjectAsset]
    ) -> "Project":
        """
        Handle the creation of asset dict
        """
        assets = {type: [] for type in schema.ResourceType}
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


class ProjectMetadata(schema.Project):
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
