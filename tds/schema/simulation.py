"""
API schema for simulation objects
"""
# pylint: disable=missing-class-docstring

from json import dumps
from typing import List, Optional

from tds.autogen import orm
from tds.modules.model_configuration.model import ModelConfiguration
from tds.modules.simulation.model import Simulation
from tds.schema.concept import Concept

SimulationParameters = List[dict]


def orm_to_params(parameters: List) -> SimulationParameters:
    """
    Convert SQL parameter search to dict
    """
    return [
        {"name": param.name, "value": param.value, "type": param.type, "id": param.id}
        for param in parameters
    ]
