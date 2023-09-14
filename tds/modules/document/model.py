"""
TDS Document Data Model Definition.
"""
from typing import Any, List, Optional

from pydantic import AnyUrl, BaseModel, Field

from tds.db.base import TdsModel
from tds.modules.dataset.model import Grounding


class Asset(BaseModel):
    """
    Asset class for storing document assets in TDS.
    """

    file_name: str = Field(description="The file name of the asset")
    metadata: Optional[dict[str, Any]] = Field(
        description="(Optional) Unformatted metadata field that should contain the asset type of the object under a 'type' key. Supported types are currently: 'equations', 'images', and 'figures'"
    )


class Document(TdsModel):
    """
    Document Data Model
    """

    _index = "document"

    username: str = Field(
        description="The username of the user that created the document."
    )
    name: str = Field(description="Display/human name for the document")
    description: Optional[str] = Field(
        description="(Optional) Texual description of the document"
    )
    file_names: List[str] = Field(description="List of file names used for storage")
    document_url: Optional[AnyUrl] = Field(
        description="(Optional) Url from which the document can be downloaded/fetched (e.g. xDD URI)"
    )
    metadata: Optional[dict[str, Any]] = Field(
        description="(Optional) Unformatted metadata about the dataset"
    )
    source: Optional[str] = Field(description="(Optional) Source of document")
    text: Optional[str] = Field(
        description="(Optional) Plain text extracted from the document"
    )
    grounding: Optional[Grounding] = Field(
        description="(Optional) Grounding of ontological concepts related to the document"
    )
    concepts: Optional[List] = []
    assets: Optional[List[Asset]] = Field(
        description="(Optional) List of assets extracted from the document by Cosmos, containing file names and metadata about each asset"
    )

    class Config:
        """
        Document Data Model Swagger Example
        """

        schema_extra = {
            "example": {
                "id": "sidarthe",
                "name": "SIDARTHE - Lack of practical identifiability may hamper reliable predictions in COVID-19 epidemic models",
                "username": "Adam Smith",
                "description": "string",
                "timestamp": "2023-08-30T14:53:12.994Z",
                "file_names": ["paper.pdf"],
                "metadata": {},
                "document_url": "https://github.com/DARPA-ASKEM/knowledge-middleware/blob/main/tests/scenarios/sidarthe/paper.pdf",
                "source": "Science Advances",
                "text": "INTRODUCTION\nThe pandemic caused by severe acute respiratory syndrome\ncoronavirus-2 is challenging humanity in an unprecedented way\n(1), with the disease, which in a few months has spread around the\nworld, affecting large parts of the population (2, 3) and often requir-\ning hospitalization or even intensive care (4, 5). Mitigating the impact\nof coronavirus disease 2019 (COVID-19) urges synergistic efforts to\nunderstand, predict, and control the many, often elusive, facets of\n...",
                "grounding": {"identifiers": {}, "context": {}},
            }
        }
