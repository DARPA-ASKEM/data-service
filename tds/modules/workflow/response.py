"""
TDS Model Configuration Response object.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class WorkflowResponse(BaseModel):
    """
    Model Configuration Response Object.
    """

    id: str
    name: str
    description: str
    timestamp: datetime
    nodes: Optional[List]
    configuration: object


def workflow_response(workflow_list):
    """
    Function builds list of model configs for response.
    """
    return [WorkflowResponse(**x["_source"]) for x in workflow_list]
