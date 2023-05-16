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


class DatasetColumn(BaseModel):
    name: str = Field(
        title="Name",
        description="Name of column"
    )
    data_type: ColumnTypes = Field(
        default=ColumnTypes.unknown,
        description=f"Datatype. One of: {', '.join(ColumnTypes)}"
    )
    format_str: Optional[str] = Field(
        description="String that describes the formatting of the value."
    )
    # format_str_type
    annotations: list[str] = Field(
    )
    metadata: dict[str, Any] = Field(
    )


class DatasetDocument(BaseModel):
    name: str = Field(
    )
    description: Optional[str] = Field(
    )
    data_url: Optional[AnyUrl] = Field(
    )
    columns: list[DatasetColumn] = Field(
    )
    metatada: dict[str, Any] = Field(
    )
    source: Optional[str] = Field(
    )



if __name__ == "__main__":
    import json
    with open("dataset-schema.json", "w") as json_schema_file:
        json.dump(DatasetDocument.schema(), json_schema_file, indent=4)
