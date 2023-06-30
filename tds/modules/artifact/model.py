"""
TDS Artifact Data Model Definition.
"""
from typing import Any, List, Optional

from pydantic import Field

from tds.db.base import TdsModel


class Artifact(TdsModel):
    """
    Artifact Data Model
    """

    username: str = Field(
        description="The username of the user that created the artifact."
    )
    name: str = Field(
        description="Display/human name for the artifact",
    )
    description: Optional[str] = Field(
        description="(Optional) Texual description of the artifact",
    )
    file_names: List[str] = Field(
        description="List of file names used for storage",
    )
    metadata: Optional[dict[str, Any]] = Field(
        description="(Optional) Unformatted metadata about the dataset",
    )

    _index = "artifact"
    concepts: Optional[List] = []

    class Config:
        """
        Artifact Data Model Swagger Example
        """

        schema_extra = {
            "example": {
                "username": "Adam Smith",
                "name": "Test Artifact",
                "description": "Random zip to test artifact.",
                "file_names": ["test.zip"],
                "metadata": {},
            }
        }
