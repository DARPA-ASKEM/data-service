"""
TDS equation Response object.
"""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from tds.modules.equation.model import EquationSource, TypeEnum


class EquationResponse(BaseModel):
    """
    equation Response Object.
    """

    id: str
    name: str
    username: Optional[str]
    description: Optional[str]
    timestamp: datetime
    equation_type: TypeEnum
    content: str
    metadata: Optional[dict[str, Any]]
    source: Optional[EquationSource]


def equation_response(equation_list):
    """
    Function builds list of equations for response.
    """
    return [EquationResponse(**x["_source"]) for x in equation_list]
