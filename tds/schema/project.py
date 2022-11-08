"""
tds.schema.project - Provides the API interface for models.
"""
# pylint: disable=missing-class-docstring
from typing import List, Optional

from tds.autogen import orm, schema
from tds.schema.concept import Concept
from tds.schema.resources import Resource


class Asset(schema.ProjectAsset):
    class Config:
        orm_mode = True


class Project(schema.Project):
    concept: Optional[Concept] = None
    assets: List[Resource] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "Lorem ipsum dolor sit amet.",
                "assets": [],
                "status": "Active",
            }
        }
