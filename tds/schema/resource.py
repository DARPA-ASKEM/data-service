"""
Redirects general types to restricted resource typing
"""
# pylint: disable=missing-class-docstring, unhashable-member

from collections import defaultdict
from typing import Dict, Optional, Type

from tds.db.enums import ResourceType
from tds.modules.artifact.model import Artifact
from tds.modules.dataset.model import Dataset
from tds.modules.external.model import Publication as PublicationModel
from tds.modules.external.model import PublicationPayload, SoftwarePayload
from tds.modules.model.model import Model
from tds.modules.model_configuration.model import ModelConfiguration
from tds.modules.simulation.model import Simulation
from tds.modules.workflow.model import Workflow


class Publication(PublicationPayload):
    class Config:
        orm_mode = True


class Software(SoftwarePayload):
    class Config:
        orm_mode = True


Resource = Dataset | Model | ModelConfiguration | Publication | Simulation | Workflow

ORMResource = Dataset | PublicationModel | Simulation

obj_to_enum: Dict[Type[Resource], ResourceType] = {
    Dataset: ResourceType.datasets,
    Model: ResourceType.models,
    ModelConfiguration: ResourceType.model_configurations,
    Publication: ResourceType.publications,
    Simulation: ResourceType.simulations,
    Workflow: ResourceType.workflows,
    Artifact: ResourceType.artifacts,
}

obj_to_enum_desc: Dict[Type[Resource], ResourceType] = {
    Dataset: ResourceType.datasets,
    Model: ResourceType.models,
    ModelConfiguration: ResourceType.model_configurations,
    Publication: ResourceType.publications,
    Simulation: ResourceType.simulations,
    Workflow: ResourceType.workflows,
    Artifact: ResourceType.artifacts,
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
            ResourceType.datasets: Dataset,
            ResourceType.publications: PublicationModel,
            ResourceType.simulations: Simulation,
        },
    )
    return enum_to_orm[resource_type]
