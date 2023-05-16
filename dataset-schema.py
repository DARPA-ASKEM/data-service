from pydantic import BaseModel, AnyUrl, Field, UUID4
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
        description="Ontological identifier per DKG",
    )
    context: Optional[dict[str, Any]] = Field(
        description="(Optional) Additional context that informs the grounding",
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
        description="(Optional) String that describes the formatting of the value",
    )
    # format_str_type
    annotations: list[str] = Field(
        description="Column annotations from the MIT data profiling tool",
    )
    metadata: Optional[dict[str, Any]] = Field(
        description="(Optional) Unformatted metadata about the dataset",
    )
    grounding: Optional[dict[str, Grounding]] = Field(
        description="(Optional) Grounding of ontological concepts related to the column",
    )


class DatasetDocument(BaseModel):
    id: UUID4 = Field(
        description="Universally unique identifier for the dataset",
    )
    name: str = Field(
        description="Display/human name for the dataset",
    )
    description: Optional[str] = Field(
        description="(Optional) Texual description of the dataset",
    )
    data_url: Optional[AnyUrl] = Field(
        description="(Optional) Url from which the dataset can be downloaded/fetched",
    )
    columns: list[DatasetColumn] = Field(
        description="Information regarding the columns that make up the dataset",
    )
    metadata: Optional[dict[str, Any]] = Field(
        description="(Optional) Unformatted metadata about the dataset",
    )
    source: Optional[str] = Field(
        description="(Optional) Source of dataset",
    )
    grounding: Optional[dict[str, Grounding]] = Field(
        description="(Optional) Grounding of ontological concepts related to the dataset as a whole",
    )



if __name__ == "__main__":
    import json
    with open("dataset-schema.json", "w") as json_schema_file:
        json.dump(DatasetDocument.schema(), json_schema_file, indent=4)
