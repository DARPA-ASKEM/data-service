"""
tds.schema.simulations - API schema for simulation objects
"""
# pylint: disable=missing-class-docstring

from typing import Dict, List, Optional, Tuple

from tds.autogen import orm, schema
from tds.autogen.schema import SimulationPlan, SimulationRun
from tds.schema.concept import Concept


class Plan(SimulationPlan):
    concept: Optional[Concept] = None
    parameters: Dict[str, Tuple[str, schema.ValueType]] = {}

    @classmethod
    def from_orm(
        cls, body: orm.SimulationPlan, parameters: List[orm.ModelParameter]
    ) -> "Plan":
        """
        Handle ORM conversion while coercing `dict` to JSON
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
                "name": "Foo",
                "description": "Lorem ipsum dolor sit amet.",
                "content": "[]",
                "parameters": {"epsilon": "int"},
            }
        }


class Results(SimulationRun):
    class Config:
        orm_mode = True
