"""
TDS Framework Response object.
"""
from datetime import datetime

from pydantic import BaseModel


class ModelFrameworkResponse(BaseModel):
    """
    Framework Response Object.
    """

    id: str
    name: str
    description: str
    timestamp: datetime
