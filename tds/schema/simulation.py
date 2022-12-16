"""
API schema for simulation objects
"""
# pylint: disable=missing-class-docstring

from json import dumps
from typing import List, Optional

from tds.autogen import orm
from tds.autogen.schema import SimulationPlan, SimulationRun
from tds.schema.concept import Concept

SimulationParameters = List[dict]


def orm_to_params(parameters: List[orm.SimulationParameter]) -> SimulationParameters:
    """
    Convert SQL parameter search to dict
    """
    return [
        {"name": param.name, "value": param.value, "type": param.type, "id": param.id}
        for param in parameters
    ]


class Plan(SimulationPlan):
    concept: Optional[Concept] = None

    @classmethod
    def from_orm(cls, body: orm.SimulationRun) -> "Plan":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        body.__dict__["content"] = dumps(body.content)
        return super().from_orm(body)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "string",
                "simulator": "string",
                "model_id": "int",
                "dataset_id": "int",
                "query": "string",
                "content": "json-in-string",
            }
        }


class RunDescription(SimulationRun):
    class Config:
        orm_mode = True


class Run(SimulationRun):
    parameters: SimulationParameters = {}

    @classmethod
    def from_orm(
        cls, body: orm.SimulationRun, parameters: List[orm.SimulationParameter]
    ) -> "Run":
        """
        Handle ORM conversion while including parameters
        """
        setattr(
            body,
            "parameters",
            orm_to_params(parameters),
        )
        return super().from_orm(body)

    class Config:
        orm_mode = True
