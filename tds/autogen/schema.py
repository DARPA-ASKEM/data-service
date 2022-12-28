from enum import Enum
import datetime
from typing import Optional
from pydantic import BaseModel, Json


class ResourceType(str, Enum):

    datasets = 'datasets'
    intermediates = 'intermediates'
    models = 'models'
    plans = 'plans'
    publications = 'publications'
    simulation_runs = 'simulation_runs'
    

class ProvenanceType(str, Enum):

    datasets = 'datasets'
    intermediates = 'intermediates'
    model_revisions = 'model_revisions'
    models = 'models'
    plans = 'plans'
    publications = 'publications'
    simulation_runs = 'simulation_runs'
    

class RelationType(str, Enum):

    BEGINS_AT = 'BEGINS_AT'
    CITES = 'CITES'
    COMBINED_FROM = 'COMBINED_FROM'
    COPIED_FROM = 'COPIED_FROM'
    DERIVED_FROM = 'DERIVED_FROM'
    EDITED_FROM = 'EDITED_FROM'
    EQUIVALENT_OF = 'EQUIVALENT_OF'
    EXTRACTED_FROM = 'EXTRACTED_FROM'
    GENERATED_BY = 'GENERATED_BY'
    REINTERPRETS = 'REINTERPRETS'
    USES = 'USES'
    

class TaggableType(str, Enum):

    datasets = 'datasets'
    features = 'features'
    intermediates = 'intermediates'
    model_parameters = 'model_parameters'
    models = 'models'
    projects = 'projects'
    publications = 'publications'
    qualifiers = 'qualifiers'
    simulation_parameters = 'simulation_parameters'
    simulation_plans = 'simulation_plans'
    simulation_runs = 'simulation_runs'
    

class ValueType(str, Enum):

    binary = 'binary'
    bool = 'bool'
    float = 'float'
    int = 'int'
    str = 'str'
    

class OntologicalField(str, Enum):

    obj = 'obj'
    unit = 'unit'
    

class IntermediateSource(str, Enum):

    mrepresentationa = 'mrepresentationa'
    skema = 'skema'
    

class IntermediateFormat(str, Enum):

    bilayer = 'bilayer'
    gromet = 'gromet'
    other = 'other'
    sbml = 'sbml'
    

class Role(str, Enum):

    author = 'author'
    contributor = 'contributor'
    maintainer = 'maintainer'
    other = 'other'
    

class ExtractedType(str, Enum):

    equation = 'equation'
    figure = 'figure'
    table = 'table'
    

class Direction(str, Enum):

    input = 'input'
    output = 'output'
    

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


class Dataset(BaseModel):

    id: Optional[int] = None
    name: str
    url: str
    description: str
    timestamp: datetime.datetime = datetime.datetime.now()
    deprecated: Optional[bool]
    sensitivity: Optional[str]
    quality: Optional[str]
    temporal_resolution: Optional[str]
    geospatial_resolution: Optional[str]
    annotations: Optional[Json]
    maintainer: int
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


class SimulationPlan(BaseModel):

    id: Optional[int] = None
    model_id: Optional[int] = None
    simulator: str
    query: str
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
    model_id: Optional[int] = None
    name: str
    type: ValueType
    default_value: Optional[str]
    state_variable: bool


class SimulationParameter(BaseModel):

    id: Optional[int] = None
    run_id: Optional[int] = None
    name: str
    value: str
    type: ValueType


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
    object_id: Optional[int] = None
    status: OntologicalField


class Provenance(BaseModel):

    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    relation_type: RelationType
    left: int
    left_type: ProvenanceType
    right: int
    right_type: ProvenanceType
    user_id: Optional[int]


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


class ModelState(BaseModel):

    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    content: Optional[Json]


class Intermediate(BaseModel):

    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    source: IntermediateSource
    type: IntermediateFormat
    content: bytes


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
