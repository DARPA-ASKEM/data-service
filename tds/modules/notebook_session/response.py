"""
TDS  Notebook Session Response object.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NotebookSessionResponse(BaseModel):
    """
    Notebook Session Response Object.
    """

    id: str
    name: Optional[str]
    description: Optional[str]
    data: dict
    timestamp: datetime


def notebook_session_response(notebook_session_list):
    """
    Function builds list of notebook_sessions for response.
    """
    return [NotebookSessionResponse(**x["_source"]) for x in notebook_session_list]
