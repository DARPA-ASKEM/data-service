"""
TDS Model Configuration Response object.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from tds.modules.workflow.model import Transform


class WorkflowResponse(BaseModel):
    """
    Workflow Response Object.
    """

    id: str
    name: str
    description: str
    timestamp: datetime
    transform: Transform
    nodes: List[dict]
    edges: Optional[List[dict]]


def workflow_response(workflow_list):
    """
    Function builds list of model configs for response.
    """
    return [WorkflowResponse(**x["_source"]) for x in workflow_list]
