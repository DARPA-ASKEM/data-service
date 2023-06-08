"""
API schema for simulation objects
"""
from typing import List

SimulationParameters = List[dict]


def orm_to_params(parameters: List) -> SimulationParameters:
    """
    Convert SQL parameter search to dict
    """
    return [
        {"name": param.name, "value": param.value, "type": param.type, "id": param.id}
        for param in parameters
    ]
