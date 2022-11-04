"""
schema.dataset - Provides the API interface for datasets.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from json import dumps
from typing import Optional

from tds.autogen import orm, schema
from tds.schema.concept import Concept


class Model(schema.Model):
    concept: Optional[Concept]
