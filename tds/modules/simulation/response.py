"""
TDS Simulation Response object.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from tds.autogen.enums import SimulationEngine, SimulationStatus


class SimulationResponse(BaseModel):
    """
    Simulation Response Object.
    """

    id: str
    name: Optional[str]
    description: Optional[str]
    timestamp: datetime
    engine: SimulationEngine
    type: str
    status: SimulationStatus
    execution_payload: dict
    start_time: Optional[datetime]
    completed_time: Optional[datetime]
    workflow_id: str
    user_id: Optional[int]
    project_id: Optional[int]
    result_files: Optional[List[str]] = []


def simulation_response(simulation_list):
    """
    Function builds list of simulations for response.
    """
    return [SimulationResponse(**x["_source"]) for x in simulation_list]
