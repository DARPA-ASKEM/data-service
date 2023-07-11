"""
TDS Person Response object.
"""
from typing import Optional

from pydantic import BaseModel


class PersonResponse(BaseModel):
    """
    Person Response Object.
    """

    id: int
    name: str
    email: str
    org: Optional[str]
    website: Optional[str]
    is_registered: bool


def person_response(person_list):
    """
    Function builds list of persons for response.
    """
    return [PersonResponse(**x["_source"]) for x in person_list]
