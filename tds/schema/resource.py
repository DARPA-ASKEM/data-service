"""
Redirects general types to restricted resource typing
"""
# pylint: disable=missing-class-docstring, unhashable-member

from collections import defaultdict
from typing import Dict, Optional, Type

from tds.autogen import orm, schema
from tds.autogen.schema import ResourceType
from tds.modules.model.model import Model
from tds.modules.model_configuration.model import ModelConfiguration
from tds.modules.workflow.model import Workflow
from tds.schema.dataset import Dataset
from tds.schema.simulation import Run, RunDescription


class Publication(schema.Publication):
    class Config:
        orm_mode = True


class Software(schema.Software):
    class Config:
        orm_mode = True


Resource = Dataset | Model | ModelConfiguration | Publication | Run | Workflow

ORMResource = orm.Dataset | orm.Publication | orm.SimulationRun

obj_to_enum: Dict[Type[Resource], ResourceType] = {
    Dataset: ResourceType.datasets,
    Model: ResourceType.models,
    ModelConfiguration: ResourceType.model_configurations,
    Publication: ResourceType.publications,
    Run: ResourceType.simulation_runs,
    Workflow: ResourceType.workflows,
}

obj_to_enum_desc: Dict[Type[Resource], ResourceType] = {
    Dataset: ResourceType.datasets,
    Model: ResourceType.models,
    ModelConfiguration: ResourceType.model_configurations,
    Publication: ResourceType.publications,
    RunDescription: ResourceType.simulation_runs,
    Workflow: ResourceType.workflows,
}


def get_schema_description(resource_type: ResourceType) -> Type[Resource]:
    """
    Maps class to schema enum for descriptions
    """
    enum_to_obj = {type: resource for resource, type in obj_to_enum_desc.items()}
    return enum_to_obj[resource_type]


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
            ResourceType.publications: orm.Publication,
            ResourceType.simulation_runs: orm.SimulationRun,
        },
    )
    return enum_to_orm[resource_type]
