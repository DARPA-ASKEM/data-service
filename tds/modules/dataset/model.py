"""
TDS Dataset
"""
from enum import Enum
from typing import Any, List, Optional

from pydantic import AnyUrl, BaseModel, Field

from tds.db.base import TdsModel

# from sqlalchemy.orm import Session
# from tds.db.relational import engine as pg_engine


class ColumnTypes(str, Enum):
    """Column type enum"""

    UNKNOWN = "unknown"
    BOOLEAN = "boolean"
    STRING = "string"
    CHAR = "string"
    INTEGER = "integer"
    INT = "integer"
    FLOAT = "float"
    DOUBLE = "double"
    TIMESTAMP = "timestamp"
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"


class Grounding(BaseModel):
    """Onotological grounding subcomponent"""

    identifiers: dict[str, str] = Field(
        description="Ontological identifier per DKG",
    )
    context: Optional[dict[str, Any]] = Field(
        description="(Optional) Additional context that informs the grounding",
    )


class DatasetColumn(BaseModel):
    """Column subcomponent"""

    name: str = Field(
        title="Name",
        description="Name of column",
    )
    data_type: ColumnTypes = Field(
        default=ColumnTypes.UNKNOWN,
        description=f"Datatype. One of: {', '.join(ColumnTypes)}",
    )
    format_str: Optional[str] = Field(
        description="(Optional) String that describes the formatting of the value",
    )
    annotations: dict[str, List[str]] = Field(
        description="Column annotations from the MIT data profiling tool",
    )
    metadata: Optional[dict[str, Any]] = Field(
        description="(Optional) Unformatted metadata about the dataset",
    )
    grounding: Optional[dict[str, Grounding]] = Field(
        description=(
            "(Optional) Grounding of ontological concepts related to the column"
        ),
    )


class Dataset(TdsModel):
    """Dataset model"""

    _index = "dataset"

    name: str = Field(
        description="Display/human name for the dataset",
    )
    description: Optional[str] = Field(
        description="(Optional) Texual description of the dataset",
    )
    dataset_url: Optional[AnyUrl] = Field(
        description="(Optional) Url from which the dataset can be downloaded/fetched",
    )
    columns: List[DatasetColumn] = Field(
        description="Information regarding the columns that make up the dataset",
    )
    metadata: Optional[dict[str, Any]] = Field(
        description="(Optional) Unformatted metadata about the dataset",
    )
    source: Optional[str] = Field(
        description="(Optional) Source of dataset",
    )
    grounding: Optional[dict[str, Grounding]] = Field(
        description=(
            "(Optional) Grounding of ontological concepts related to the dataset as",
            " a whole",
        ),
    )

    class Config:
        """Config"""

        # schema_extra = {
        #     "example": {
        #     }
        # }

    # def _extract_concepts(self):
    #     """
    #     Method extracts concepts from the dataset and saves them to the db.
    #     """
    #     curies = []
    #     with Session(pg_engine) as pg_db:
    #         pass

    # def _establish_provenance(self):
    #     pass
