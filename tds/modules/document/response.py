"""
TDS Document Response object.
"""
from datetime import datetime
from typing import Any, List, Optional

from pydantic import AnyUrl, BaseModel

from tds.modules.dataset.model import Grounding
from tds.modules.document.model import Asset


class DocumentResponse(BaseModel):
    """
    Document Response Object.
    """

    id: str
    name: str
    username: Optional[str]
    description: Optional[str]
    timestamp: datetime
    file_names: List[str]
    metadata: Optional[dict[str, Any]]
    document_url: Optional[AnyUrl]
    source: Optional[str]
    text: Optional[str]
    grounding: Optional[Grounding]
    assets: Optional[List[Asset]]


def document_response(document_list):
    """
    Function builds list of documents for response.
    """
    return [DocumentResponse(**x["_source"]) for x in document_list]
