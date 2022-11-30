"""
Provides the API interface for datasets.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from typing import List, Optional

from tds.autogen import orm, schema
from tds.schema.concept import Concept


class Qualifier(schema.Qualifier):
    feature_names: List[str]
    concept: Optional[Concept]

    class Config:
        orm_mode = True


class Feature(schema.Feature):
    concept: Optional[Concept]

    class Config:
        orm_mode = True


class Dataset(schema.Dataset):
    features: List[Feature]
    qualifiers: List[Qualifier]
    concept: Optional[Concept]

    @classmethod
    def from_or_asset(cls, body: orm.Dataset) -> "Dataset":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """

        return super().from_orm(body)

    class Config:
        orm_mode = True
