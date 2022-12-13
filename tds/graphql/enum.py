"""
Scalar Schema
"""

# pylint: disable=invalid-name

from enum import Enum
from logging import Logger

import strawberry

from tds.autogen import schema

logger = Logger(__name__)


@strawberry.enum
class ValueType(Enum):
    """
    Possible value types duplicated from the autogen schema
    """

    binary = schema.ValueType.binary.name
    bool = schema.ValueType.bool.name
    float = schema.ValueType.float.name
    int = schema.ValueType.int.name
    str = schema.ValueType.str.name


@strawberry.enum
class TaggableType(Enum):
    """
    Possible taggable types duplicated from the autogen schema
    """

    datasets = schema.TaggableType.datasets.name
    features = schema.TaggableType.features.name
    intermediates = schema.TaggableType.intermediates.name
    model_parameters = schema.TaggableType.model_parameters.name
    models = schema.TaggableType.models.name
    projects = schema.TaggableType.projects.name
    publications = schema.TaggableType.publications.name
    qualifiers = schema.TaggableType.qualifiers.name
    simulation_parameters = schema.TaggableType.simulation_parameters.name
    simulation_plans = schema.TaggableType.simulation_plans.name
    simulation_runs = schema.TaggableType.simulation_runs.name


@strawberry.enum
class OntologicalField(Enum):
    """
    Possible fields duplicated from the autogen schema
    """

    obj = schema.OntologicalField.obj.name
    unit = schema.OntologicalField.unit.name
