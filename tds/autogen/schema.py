from enum import Enum
import datetime
from typing import Optional
from pydantic import BaseModel, Json


class ResourceType(str, Enum):

    datasets = 'datasets'
    model_configs = 'model_configs'
    models = 'models'
    publications = 'publications'
    simulation_runs = 'simulation_runs'
    

class ProvenanceType(str, Enum):

    Concept = 'Concept'
    Dataset = 'Dataset'
    Model = 'Model'
    ModelConfig = 'ModelConfig'
    ModelParameter = 'ModelParameter'
    ModelRevision = 'ModelRevision'
    Project = 'Project'
    Publication = 'Publication'
    SimParameter = 'SimParameter'
    SimulationRun = 'SimulationRun'
    

class ProvenanceSearchTypes(str, Enum):

    artifacts_created_by_user = 'artifacts_created_by_user'
    child_nodes = 'child_nodes'
    concept = 'concept'
    concept_counts = 'concept_counts'
    connected_nodes = 'connected_nodes'
    derived_models = 'derived_models'
    parent_model_revisions = 'parent_model_revisions'
    parent_models = 'parent_models'
    parent_nodes = 'parent_nodes'
    

class RelationType(str, Enum):

    BEGINS_AT = 'BEGINS_AT'
    CITES = 'CITES'
    COMBINED_FROM = 'COMBINED_FROM'
    CONTAINS = 'CONTAINS'
    COPIED_FROM = 'COPIED_FROM'
    DECOMPOSED_FROM = 'DECOMPOSED_FROM'
    DERIVED_FROM = 'DERIVED_FROM'
    EDITED_FROM = 'EDITED_FROM'
    EQUIVALENT_OF = 'EQUIVALENT_OF'
    EXTRACTED_FROM = 'EXTRACTED_FROM'
    GENERATED_BY = 'GENERATED_BY'
    GLUED_FROM = 'GLUED_FROM'
    IS_CONCEPT_OF = 'IS_CONCEPT_OF'
    PARAMETER_OF = 'PARAMETER_OF'
    REINTERPRETS = 'REINTERPRETS'
    STRATIFIED_FROM = 'STRATIFIED_FROM'
    USES = 'USES'
    

class ModelOperations(str, Enum):

    copy = 'copy'
    decompose = 'decompose'
    glue = 'glue'
    stratify = 'stratify'
    

class TaggableType(str, Enum):

    datasets = 'datasets'
    features = 'features'
    model_configurations = 'model_configurations'
    model_parameters = 'model_parameters'
    models = 'models'
    projects = 'projects'
    publications = 'publications'
    qualifiers = 'qualifiers'
    simulation_parameters = 'simulation_parameters'
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


class Software(BaseModel):

    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    source: str
    storage_uri: str


class SimulationRun(BaseModel):

    id: Optional[int] = None
    simulator_id: str
    timestamp: datetime.datetime = datetime.datetime.now()
    completed_at: Optional[datetime.datetime]
    success: Optional[bool]
    dataset_id: Optional[int]
    description: Optional[str]
    response: Optional[bytes]


class ModelParameter(BaseModel):

    id: Optional[int] = None
    model_id: Optional[str]
    name: str
    type: ValueType
    default_value: Optional[str]
    state_variable: bool


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
