"""
schema.dataset - Provides the API interface for datasets.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from typing import List, Optional

from src.autogen import schema
from src.schema.concept import Concept


class Qualifier(schema.Qualifier):
    feature_names: List[str]
    concept: Optional[Concept]


class Feature(schema.Feature):
    concept: Optional[Concept]


class Dataset(schema.Dataset):
    features: List[Feature]
    qualifiers: List[Qualifier]
    concept: Optional[Concept]
