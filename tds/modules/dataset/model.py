"""
TDS Dataset
"""
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import AnyUrl, BaseModel, Field

from tds.autogen.orm import Base
from tds.db.base import TdsModel


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
    description: Optional[str] = Field(
        description="(Optional) Textual description of the dataset column.",
    )
    format_str: Optional[str] = Field(
        description="(Optional) String that describes the formatting of the value",
    )
    annotations: List[str] = Field(
        description="Column annotations from the MIT data profiling tool",
    )
    metadata: Optional[dict[str, Any]] = Field(
        description="(Optional) Unformatted metadata about the dataset",
    )
    grounding: Optional[Grounding] = Field(
        description=(
            "(Optional) Grounding of ontological concepts related to the column"
        ),
    )


class Dataset(TdsModel):
    """Dataset model"""

    _index = "dataset"

    username: str = Field(
        description="The username of the user that created the dataset."
    )
    name: str = Field(
        description="Display/human name for the dataset",
    )
    description: Optional[str] = Field(
        description="(Optional) Textual description of the dataset",
    )
    data_source_date: Optional[datetime] = Field(
        description="(Optional) The date the data was created."
    )
    file_names: List[str] = Field(
        description="List of file names used for storage",
    )
    dataset_url: Optional[AnyUrl] = Field(
        description="(Optional) Url from which the dataset can be downloaded/fetched",
    )
    columns: Optional[List[DatasetColumn]] = Field(
        description="Information regarding the columns that make up the dataset",
    )
    metadata: Optional[dict[str, Any]] = Field(
        description="(Optional) Unformatted metadata about the dataset",
    )
    source: Optional[str] = Field(
        description="(Optional) Source of dataset",
    )
    grounding: Optional[Grounding] = Field(
        description=(
            "(Optional) Grounding of ontological concepts related to the dataset as"
            " a whole"
        ),
    )

    class Config:
        """Config"""

        schema_extra = {
            "example": {
                "username": "Adam Smith",
                "data_source_date": "2022-10-01T12:00:00",
                "name": "CDC COVID-19 Vaccination and Case Trends by Age Group",
                "description": "CDC COVID-19 Vaccination and Case Trends by Age Group",
                "file_names": [
                    # pylint: disable-next=line-too-long
                    "Archive__COVID-19_Vaccination_and_Case_Trends_by_Age_Group__United_States.csv"
                ],
                "columns": [
                    {
                        "name": "Date Administered",
                        "data_type": "date",
                        "format_str": "MM/dd/yy",
                        "annotations": {},
                        "metadata": {},
                        "grounding": {},
                    },
                    {
                        "name": "Country",
                        "data_type": "string",
                        "annotations": {},
                        "metadata": {},
                        "grounding": {},
                    },
                    {
                        "name": "AgeGroupVacc",
                        "data_type": "string",
                        "annotations": {},
                        "metadata": {},
                        "grounding": {},
                    },
                    {
                        "name": "7-day_avg_group_cases_per_100k",
                        "data_type": "float",
                        "annotations": {},
                        "metadata": {},
                        "grounding": {},
                    },
                    {
                        "name": "Administered_Dose1_pct_agegroup",
                        "data_type": "float",
                        "annotations": {},
                        "metadata": {},
                        "grounding": {},
                    },
                    {
                        "name": "Series_Complete_Pop_pct_agegroup",
                        "data_type": "float",
                        "annotations": {},
                        "metadata": {},
                        "grounding": {},
                    },
                ],
                "metadata": {},
                # pylint: disable-next=line-too-long
                "source": "https://data.cdc.gov/Vaccinations/Archive-COVID-19-Vaccination-and-Case-Trends-by-Ag/gxj9-t96f/data",
                "grounding": {
                    "additionalProp1": {"identifiers": {}, "context": {}},
                },
            }
        }

    # def _extract_concepts(self):
    #     """
    #     Method extracts concepts from the dataset and saves them to the db.
    #     """
    #     curies = []
    #     with Session(pg_engine) as pg_db:
    #         pass

    # def _establish_provenance(self):
    #     pass


class QualifierXref(Base):
    """
    QualifierXref Data Model.
    """

    __tablename__ = "qualifier_xref"

    id = sa.Column(sa.Integer(), primary_key=True)
    qualifier_id = sa.Column(
        sa.Integer(), sa.ForeignKey("qualifier.id"), nullable=False
    )
    feature_id = sa.Column(sa.Integer(), sa.ForeignKey("feature.id"), nullable=False)
