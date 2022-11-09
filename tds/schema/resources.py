"""
tds.schema.resources - Redirects general types to restricted resource typing
"""
# pylint: disable=missing-class-docstring

from typing import Any, Optional

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


def get_resource_type(resource: Resource) -> Optional[ResourceType]:
    """
    Maps class to resource enum
    """
    resource_type = None
    match resource:
        case Dataset():
            resource_type = ResourceType.dataset
        case ExtractedData():
            resource_type = ResourceType.extracted_data
        case Model():
            resource_type = ResourceType.model
        case Plan():
            resource_type = ResourceType.plan
        case Publication():
            resource_type = ResourceType.publication
        case Intermediate():
            resource_type = ResourceType.intermediate
        case _:
            resource_type = None
    return resource_type


def get_resource_orm(resource_type: ResourceType) -> Optional[ORMResource]:
    """
    Maps resource type to ORM
    """
    result_orm = None
    match resource_type:
        case ResourceType.dataset:
            result_orm = orm.Dataset
        case ResourceType.extracted_data:
            result_orm = orm.ExtractedData
        case ResourceType.model:
            result_orm = orm.Model
        case ResourceType.plan:
            result_orm = orm.SimulationPlan
        case ResourceType.publication:
            result_orm = orm.Publication
        case Intermediate():
            result_orm = orm.Intermediate
        case _:
            result_orm = None
    return result_orm
