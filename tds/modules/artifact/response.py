"""
TDS Artifact Response object.
"""
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


class ArtifactResponse(BaseModel):
    """
    Artifact Response Object.
    """

    id: str
    name: str
    username: Optional[str]
    description: Optional[str]
    timestamp: datetime
    file_names: List[str]
    metadata: Optional[dict[str, Any]]


def artifact_response(artifact_list):
    """
    Function builds list of artifacts for response.
    """
    return [ArtifactResponse(**x["_source"]) for x in artifact_list]
