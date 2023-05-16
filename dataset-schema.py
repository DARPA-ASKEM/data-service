from pydantic import BaseModel, AnyUrl, Field
from typing import Optional, Any
from enum import Enum

class ColumnTypes(str, Enum):
    unknown = "unknown"
    boolean = "boolean"
    string = "string"
    char = "char"
    integer = "integer"
    int = "int"
    float = "float"
    double = "double"
    timestamp = "timestamp"
    datetime = "datetime"
    date = "date"
    time = "time"


class Grounding(BaseModel):
    identifiers: dict[str, str] = Field(
        description="",
    )
    context: Optional[dict[str, Any]] = Field(
        description="",
    )


class DatasetColumn(BaseModel):
    name: str = Field(
        title="Name",
        description="Name of column",
    )
    data_type: ColumnTypes = Field(
        default=ColumnTypes.unknown,
        description=f"Datatype. One of: {', '.join(ColumnTypes)}",
    )
    format_str: Optional[str] = Field(
        description="String that describes the formatting of the value.",
    )
    # format_str_type
    annotations: list[str] = Field(
        description="",
    )
    metadata: dict[str, Any] = Field(
        description="",
    )
    grounding: Optional[Grounding] = Field(
        description="",
    )


class DatasetDocument(BaseModel):
    name: str = Field(
    )
    description: Optional[str] = Field(
        description="Texual description of the dataset.",
    )
    data_url: Optional[AnyUrl] = Field(
        description="Url from which the dataset can be downloaded/fetched.",
    )
    columns: list[DatasetColumn] = Field(
        description="Information regarding the columns that make up the dataset.",
    )
    metatada: Optional[dict[str, Any]] = Field(
        description="(Optional) Unformatted metadata about the dataset.",
    )
    source: Optional[str] = Field(
        description="Source of dataset",
    )
    grounding: Optional[Grounding] = Field(
        description="",
    )



if __name__ == "__main__":
    import json
    with open("dataset-schema.json", "w") as json_schema_file:
        json.dump(DatasetDocument.schema(), json_schema_file, indent=4)
