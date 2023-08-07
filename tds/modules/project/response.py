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
