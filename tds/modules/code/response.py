"""
TDS Code Response object.
"""
from datetime import datetime

from pydantic import BaseModel


class CodeResponse(BaseModel):
    """
    Code Response Object.
    """

    id: str
    name: str
    description: str
    timestamp: datetime


def code_response(code_list):
    """
    Function builds list of codes for response.
    """
    return [CodeResponse(**x["_source"]) for x in code_list]
