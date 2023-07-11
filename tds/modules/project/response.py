"""
TDS Project Response object.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectResponse(BaseModel):
    """
    ProjectResponse Class.
    """

    id: Optional[int] = None
    name: str
    description: str
    timestamp: Optional[datetime] = datetime.now()
    active: bool
    username: Optional[str]


def project_response(project_list):
    """
    Function builds list of projects for response.
    """
    return [ProjectResponse(**x["_source"]) for x in project_list]
