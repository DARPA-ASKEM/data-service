# pylint: skip-file
"""
Schema file from DBML autogen.
Skipping linter to prevent class docstring errors.
@TODO: Clean up file to pass linting.
"""
import datetime
from typing import Optional

from pydantic import BaseModel

from tds.autogen.enums import ExtractedType, OntologicalField, TaggableType, ValueType


class QualifierXref(BaseModel):
    id: Optional[int] = None
    qualifier_id: Optional[int] = None
    feature_id: Optional[int] = None


class ModelRuntime(BaseModel):
    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    name: str
    left: str
    right: str


class Feature(BaseModel):
    id: Optional[int] = None
    dataset_id: Optional[int] = None
    description: Optional[str]
    display_name: Optional[str]
    name: str
    value_type: ValueType


class Qualifier(BaseModel):
    id: Optional[int] = None
    dataset_id: Optional[int] = None
    description: Optional[str]
    name: str
    value_type: ValueType


class Extraction(BaseModel):
    id: Optional[int] = None
    publication_id: Optional[int] = None
    type: ExtractedType
    data: bytes
    img: bytes


class OntologyConcept(BaseModel):
    id: Optional[int] = None
    curie: str
    type: TaggableType
    object_id: str
    status: OntologicalField


class ModelFramework(BaseModel):
    name: str
    version: str
    semantics: str
    schema_url: Optional[str]


class Software(BaseModel):
    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    source: str
    storage_uri: str


class Publication(BaseModel):
    id: Optional[int] = None
    xdd_uri: str
    title: str
