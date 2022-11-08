"""
tds.schema.resources - Redirects general types to restricted resource typing
"""
# pylint: disable=missing-class-docstring

from typing import Optional

from tds.autogen import schema
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
