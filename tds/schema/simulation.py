"""
API schema for simulation objects
"""
# pylint: disable=missing-class-docstring

from json import dumps
from typing import Dict, List, Optional, Tuple

from tds.autogen import orm, schema
from tds.autogen.schema import SimulationPlan, SimulationRun
from tds.schema.concept import Concept


class Plan(SimulationPlan):
    concept: Optional[Concept] = None

    @classmethod
    def from_orm(cls, body: orm.SimulationRun) -> "Plan":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        setattr(body, "content", dumps(body.content))
        return super().from_orm(body)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "string",
                "simulator": "string",
                "model_id": "int",
                "query": "string",
                "content": "json-in-string",
            }
        }


class Run(SimulationRun):
    success = None
    parameters: Dict[str, Tuple[str, schema.ValueType]] = {}

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
            {param.name: (param.value, param.type) for param in parameters},
        )
        return super().from_orm(body)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "simulator_id": 0,
                "timestamp": "datetime",
                "completed_at": "optional-datetime",
                "response": "blob",
                "parameters": {"str": ("str", "value-type")},
            }
        }
