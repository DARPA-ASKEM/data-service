"""
TDS Code Response object.
"""
from typing import Dict, Optional

from pydantic import BaseModel

from tds.db.enums import ProgrammingLanguage


class CodeResponse(BaseModel):
    """
    Code Response Object.
    """

    id: str
    name: str
    description: str
    files: Optional[Dict]
    repo_url: Optional[str]
    commit: Optional[str]
    branch: Optional[str]
    metadata: Optional[dict]


def code_response(code_list):
    """
    Function builds list of codes for response.
    """
    return [CodeResponse(**x["_source"]) for x in code_list]
