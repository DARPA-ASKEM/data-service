"""
tds.schema.project - Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from collections import defaultdict
from typing import Dict, List, Optional, Set

from tds.autogen import orm, schema
from tds.schema.concept import Concept


class Asset(schema.ProjectAsset):
    class Config:
        orm_mode = True


class Project(schema.Project):
    concept: Optional[Concept] = None
    assets: Dict[schema.ResourceType, Set[int]] = {}

    @classmethod
    def from_orm(
        cls, body: orm.Project, project_assets: List[orm.ProjectAsset]
    ) -> "Project":
        """
        Handle the creation of asset dict
        """
        assets = defaultdict(list)
        for asset in project_assets:
            assets[asset.resource_type].append(asset.resource_id)

        setattr(body, "assets", assets)
        return super().from_orm(body)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "string",
                "description": "string",
                "assets": {"resource-type": "list-of-ordered-ints"},
                "status": "string",
            }
        }
