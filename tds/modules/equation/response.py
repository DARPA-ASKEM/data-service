"""
TDS equation Response object.
"""
from datetime import datetime
from typing import Any, List, Optional

from pydantic import AnyUrl, BaseModel

from tds.modules.dataset.model import Grounding
from tds.modules.equation.model import EquationSource, TypeEnum


class equationResponse(BaseModel):
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
    return [equationResponse(**x["_source"]) for x in equation_list]
