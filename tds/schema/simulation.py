"""
tds.schema.simulations - API schema for simulation object
"""
# pylint: disable=missing-class-docstring

from tds.autogen.schema import SimulationPlan


class Plan(SimulationPlan):
    class Config:
        orm_mode = True
