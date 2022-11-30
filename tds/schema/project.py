"""
Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from collections import defaultdict
from typing import Dict, List, Optional, Set

from tds.autogen import orm, schema
from tds.schema.concept import Concept


class Project(schema.Project):
    concept: Optional[Concept] = None
    active = True
    assets: Dict[schema.ResourceType, dict] = {}

    @classmethod
    def from_orm(cls, body: orm.Project, project_assets) -> "Project":
        """
        Handle the creation of asset dict
        """
        # assets = defaultdict(list)
        # for asset in project_assets:
        #     assets[asset.resource_type].append(asset)

        setattr(body, "assets", project_assets)
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
