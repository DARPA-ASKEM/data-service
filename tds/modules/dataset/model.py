"""
TDS Dataset
"""
from datetime import datetime
from typing import Any, List, Optional

import sqlalchemy as sa
from pydantic import AnyUrl, BaseModel, Field

from tds.db.base import BaseElasticSearchModel, RelationalDatabaseBase
from tds.db.enums import ColumnTypes, ValueType


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


class Dataset(BaseElasticSearchModel):
    """Dataset model"""

    _index = "dataset"

    username: Optional[str] = Field(
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
                        "annotations": [],
                    },
                    {
                        "name": "Country",
                        "data_type": "string",
                        "annotations": [],
                        "metadata": {},
                        "grounding": {
                            "identifiers": {"onto:123": "epi_concept_here"},
                        },
                    },
                    {
                        "name": "AgeGroupVacc",
                        "data_type": "string",
                        "annotations": [],
                        "metadata": {},
                        "grounding": {
                            "identifiers": {"onto:123": "epi_concept_here"},
                        },
                    },
                    {
                        "name": "7-day_avg_group_cases_per_100k",
                        "data_type": "float",
                        "annotations": [],
                        "metadata": {},
                    },
                    {
                        "name": "Administered_Dose1_pct_agegroup",
                        "data_type": "float",
                        "annotations": [],
                        "metadata": {},
                    },
                    {
                        "name": "Series_Complete_Pop_pct_agegroup",
                        "data_type": "float",
                        "annotations": [],
                        "metadata": {},
                    },
                ],
                "metadata": {},
                # pylint: disable-next=line-too-long
                "source": "https://data.cdc.gov/Vaccinations/Archive-COVID-19-Vaccination-and-Case-Trends-by-Ag/gxj9-t96f/data",
                "groundings": {
                    "identifiers": {
                        "oboinowl:date": "date",
                        "dc:date": "Date",
                        "opmi:0000488": "visit end date",
                        "opmi:0000510": "procedure end date",
                    }
                },
            }
        }


class QualifierXref(RelationalDatabaseBase):
    """
    QualifierXref Data Model.
    """

    __tablename__ = "qualifier_xref"

    id = sa.Column(sa.Integer(), primary_key=True)
    qualifier_id = sa.Column(
        sa.Integer(), sa.ForeignKey("qualifier.id"), nullable=False
    )
    feature_id = sa.Column(sa.Integer(), sa.ForeignKey("feature.id"), nullable=False)


class QualifierXrefPayload(BaseModel):
    """
    QualifierXref Payload Model.
    """

    id: Optional[int] = None
    qualifier_id: Optional[int] = None
    feature_id: Optional[int] = None


class Qualifier(RelationalDatabaseBase):
    """
    Qualifier Data Model.
    """

    __tablename__ = "qualifier"

    id = sa.Column(sa.Integer(), primary_key=True)
    dataset_id = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.Text())
    name = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.Enum(ValueType), nullable=False)


class QualifierPayload(BaseModel):
    """
    Qualifier Payload Model.
    """

    id: Optional[int] = None
    dataset_id: Optional[str] = None
    description: Optional[str]
    name: str
    value_type: ValueType


class Feature(RelationalDatabaseBase):
    """
    Feature Data Model.
    """

    __tablename__ = "feature"

    id = sa.Column(sa.Integer(), primary_key=True)
    dataset_id = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.Text())
    display_name = sa.Column(sa.String())
    name = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.Enum(ValueType), nullable=False)


class FeaturePayload(BaseModel):
    """
    Feature Payload Model.
    """

    id: Optional[int] = None
    dataset_id: Optional[str] = None
    description: Optional[str]
    display_name: Optional[str]
    name: str
    value_type: ValueType
