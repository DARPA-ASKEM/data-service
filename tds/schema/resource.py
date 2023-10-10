"""
Redirects general types to restricted resource typing
"""
# pylint: disable=missing-class-docstring, unhashable-member

from collections import defaultdict
from typing import Dict, Optional, Type

from tds.db.enums import ResourceType
from tds.modules.artifact.model import Artifact
from tds.modules.code.model import Code
from tds.modules.dataset.model import Dataset
from tds.modules.document.model import Document
from tds.modules.external.model import Publication, SoftwarePayload
from tds.modules.model.model import Model
from tds.modules.model_configuration.model import ModelConfiguration
from tds.modules.simulation.model import Simulation
from tds.modules.workflow.model import Workflow


class Software(SoftwarePayload):
    class Config:
        orm_mode = True


Resource = (
    Code
    | Dataset
    | Document
    | Model
    | ModelConfiguration
    | Publication
    | Simulation
    | Workflow
)

ORMResource = Dataset | Publication | Simulation

obj_to_enum: Dict[Type[Resource], ResourceType] = {
    Artifact: ResourceType.artifacts,
    Code: ResourceType.code,
    Dataset: ResourceType.datasets,
    Document: ResourceType.documents,
    Model: ResourceType.models,
    ModelConfiguration: ResourceType.model_configurations,
    Publication: ResourceType.publications,
    Simulation: ResourceType.simulations,
    Workflow: ResourceType.workflows,
}


def get_resource_type(resource: Resource) -> Optional[ResourceType]:
    """
    Maps class to resource enum
    """
    return obj_to_enum.get(type(resource), None)


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
    enum_to_orm = {
        enum_value: r_type
        for r_type, enum_value in obj_to_enum.items()
        if issubclass(r_type, ORMResource)
    }
    return enum_to_orm.get(resource_type, None)
