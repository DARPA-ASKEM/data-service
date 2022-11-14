"""
tds.schema.resource - Redirects general types to restricted resource typing
"""
# pylint: disable=missing-class-docstring, unhashable-member

from collections import defaultdict
from typing import Dict, Optional, Type

from tds.autogen import orm, schema
from tds.autogen.schema import ResourceType
from tds.schema.dataset import Dataset
from tds.schema.model import Model
from tds.schema.simulation import Plan


class ExtractedData(schema.ExtractedData):
    class Config:
        orm_mode = True


class Publication(schema.Publication):
    class Config:
        orm_mode = True


class Intermediate(schema.Intermediate):
    class Config:
        orm_mode = True


Resource = Dataset | ExtractedData | Model | Plan | Publication | Intermediate
ORMResource = (
    orm.Dataset
    | orm.ExtractedData
    | orm.Model
    | orm.SimulationPlan
    | orm.Publication
    | orm.Intermediate
)


obj_to_enum: Dict[Type[Resource], ResourceType] = {
    Dataset: ResourceType.dataset,
    ExtractedData: ResourceType.extracted_data,
    Model: ResourceType.model,
    Plan: ResourceType.plan,
    Publication: ResourceType.publication,
    Intermediate: ResourceType.intermediate,
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
            ResourceType.dataset: orm.Dataset,
            ResourceType.extracted_data: orm.ExtractedData,
            ResourceType.model: orm.Model,
            ResourceType.plan: orm.SimulationPlan,
            ResourceType.publication: orm.Publication,
            ResourceType.intermediate: orm.Intermediate,
        },
    )
    return enum_to_orm[resource_type]
