"""
Provides the API interface for datasets.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from typing import List, Optional

from tds.modules.dataset.model import FeaturePayload, QualifierPayload
from tds.schema.concept import Concept


class Qualifier(QualifierPayload):
    feature_names: List[str]
    concept: Optional[Concept]

    class Config:
        orm_mode = True


class Feature(FeaturePayload):
    concept: Optional[Concept]

    class Config:
        orm_mode = True
