# pylint: skip-file
"""
Schema file from DBML autogen.
Skipping linter to prevent class docstring errors.
@TODO: Clean up file to pass linting.
"""
import datetime
from typing import Optional
from pydantic import BaseModel, Json
from tds.autogen.enums import (
    ExtractedType,
    OntologicalField,
    ProvenanceType,
    RelationType,
    ResourceType,
    Role,
    TaggableType,
    ValueType,
)


class QualifierXref(BaseModel):
    id: Optional[int] = None
    qualifier_id: Optional[int] = None
    feature_id: Optional[int] = None


class ModelDescription(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str]
    framework: str
    timestamp: datetime.datetime = datetime.datetime.now()
    state_id: Optional[int] = None


class ModelRuntime(BaseModel):
    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    name: str
    left: str
    right: str


class SimulationParameter(BaseModel):
    id: Optional[int] = None
    run_id: Optional[int] = None
    model_parameter_id: Optional[int]
    name: str
    value: str
    type: ValueType


class Dataset(BaseModel):
    id: Optional[int] = None
    name: str
    url: str
    description: str
    timestamp: datetime.datetime = datetime.datetime.now()
    deprecated: Optional[bool] = False
    sensitivity: Optional[str]
    quality: Optional[str]
    temporal_resolution: Optional[str]
    geospatial_resolution: Optional[str]
    annotations: Optional[Json]
    data_path: Optional[str]
    maintainer: Optional[int]
    simulation_run: Optional[bool] = False


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


class ModelConfiguration(BaseModel):
    id: Optional[int] = None
    model_id: Optional[int] = None
    name: str
    content: Json


class SimulationRun(BaseModel):
    id: Optional[int] = None
    simulator_id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    completed_at: Optional[datetime.datetime]
    success: Optional[bool]
    dataset_id: Optional[int]
    description: Optional[str]
    response: Optional[bytes]


class ModelParameter(BaseModel):
    id: Optional[int] = None
    model_id: Optional[int]
    name: str
    type: ValueType
    default_value: Optional[str]
    state_variable: bool


class Extraction(BaseModel):
    id: Optional[int] = None
    publication_id: Optional[int] = None
    type: ExtractedType
    data: bytes
    img: bytes


class ProjectAsset(BaseModel):
    id: Optional[int] = None
    project_id: Optional[int] = None
    resource_id: Optional[int] = None
    resource_type: ResourceType
    external_ref: Optional[str]


class OntologyConcept(BaseModel):
    id: Optional[int] = None
    curie: str
    type: TaggableType
    object_id: str
    status: OntologicalField


class Provenance(BaseModel):
    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    relation_type: RelationType
    left: str
    left_type: ProvenanceType
    right: str
    right_type: ProvenanceType
    user_id: Optional[int]
    concept: Optional[str]


class Association(BaseModel):
    id: Optional[int] = None
    person_id: Optional[int] = None
    resource_id: Optional[int] = None
    resource_type: Optional[ResourceType]
    role: Optional[Role]


class ModelFramework(BaseModel):
    name: str
    version: str
    semantics: str
    schema_url: Optional[str]


class ModelState(BaseModel):
    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    content: Optional[Json]


class Software(BaseModel):
    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    source: str
    storage_uri: str


class Publication(BaseModel):
    id: Optional[int] = None
    xdd_uri: str
    title: str


class Project(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    timestamp: Optional[datetime.datetime] = datetime.datetime.now()
    active: bool
    username: Optional[str]


class Person(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    org: Optional[str]
    website: Optional[str]
    is_registered: bool


class ActiveConcept(BaseModel):
    curie: str
    name: Optional[str]
