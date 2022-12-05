"""
Provides the API interface for datasets.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from typing import List, Optional

from tds.autogen import schema
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
    simulation_run: bool = False

    class Config:
        orm_mode = True
