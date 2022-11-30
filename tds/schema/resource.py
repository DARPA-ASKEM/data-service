"""
Redirects general types to restricted resource typing
"""
# pylint: disable=missing-class-docstring, unhashable-member

from collections import defaultdict
from typing import Dict, Optional, Type

from tds.autogen import orm, schema
from tds.autogen.schema import ResourceType
from tds.schema.dataset import Dataset
from tds.schema.model import Intermediate, Model
from tds.schema.simulation import Plan, Run


class Extraction(schema.Extraction):
    class Config:
        orm_mode = True


class Publication(schema.Publication):
    class Config:
        orm_mode = True


class Software(schema.Software):
    class Config:
        orm_mode = True


Resource = Dataset | Extraction | Model | Plan | Publication | Intermediate | Run

ORMResource = (
    orm.Dataset
    | orm.Extraction
    | orm.Model
    | orm.SimulationPlan
    | orm.Publication
    | orm.Intermediate
    | orm.SimulationRun
)

obj_to_enum: Dict[Type[Resource], ResourceType] = {
    Dataset: ResourceType.datasets,
    Extraction: ResourceType.extractions,
    Model: ResourceType.models,
    Plan: ResourceType.plans,
    Publication: ResourceType.publications,
    Intermediate: ResourceType.intermediates,
    Run: ResourceType.simulation_runs,
}


def get_resource_type(resource: Resource) -> Optional[ResourceType]:
    """
    Maps class to resource enum
    """
    return defaultdict(lambda: None, obj_to_enum)[type(resource)]


def get_schema(resource_type: ResourceType) -> Type[Resource]:
    """
    Maps class to resource enum
    """
    enum_to_obj = {type: resource for resource, type in obj_to_enum.items()}
    return enum_to_obj[resource_type]


def get_resource_orm(resource_type: ResourceType) -> Optional[ORMResource]:
    """
    Maps resource type to ORM
    """
    enum_to_orm = defaultdict(
        lambda: None,
        {
            ResourceType.datasets: orm.Dataset,
            ResourceType.extractions: orm.Extraction,
            ResourceType.models: orm.Model,
            ResourceType.plans: orm.SimulationPlan,
            ResourceType.publications: orm.Publication,
            ResourceType.intermediates: orm.Intermediate,
            ResourceType.simulation_runs: orm.SimulationRun,
        },
    )
    return enum_to_orm[resource_type]


def map_resource_str_orm(resource_type: str) -> Optional[ORMResource]:
    """
    Maps resource type to ORM
    """
    enum_to_orm = defaultdict(
        lambda: None,
        {
            "datasets": orm.Dataset,
            "extractions": orm.Extraction,
            "models": orm.Model,
            "plans": orm.SimulationPlan,
            "publications": orm.Publication,
            "intermediates": orm.Intermediate,
            "simulation_runs": orm.SimulationRun,
        },
    )
    return enum_to_orm[resource_type]
