"""
tds.schema.project - Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from collections import defaultdict
from typing import Dict, List, Optional

from tds.autogen import orm, schema
from tds.schema.concept import Concept


class Project(schema.Project):
    concept: Optional[Concept] = None
    assets: Dict[schema.ResourceType, List[int]] = {}

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
                "name": "Foo",
                "description": "Lorem ipsum dolor sit amet.",
                "assets": {},
                "status": "Active",
            }
        }
