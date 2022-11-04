from typing import Optional, Type

from pydantic import BaseModel

from tds.autogen.schema import (
    ExtractedData,
    Intermediate,
    Publication,
    ResourceType,
    SimulationPlan,
)
from tds.schema.dataset import Dataset
from tds.schema.model import Model


def get_resource_type(resource: Type[BaseModel]) -> Optional[ResourceType]:
    match resource.__qualname__:
        case Dataset.__qualname__:
            return ResourceType.dataset
        case ExtractedData.__qualname__:
            return ResourceType.extracted_data
        case Model.__qualname__:
            return ResourceType.model
        case SimulationPlan.__qualname__:
            return ResourceType.plan
        case Publication.__qualname__:
            return ResourceType.publication
        case Intermediate.__qualname__:
            return ResourceType.intermediate
        case _:
            return None
