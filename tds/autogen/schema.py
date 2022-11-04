from enum import Enum
import datetime
from typing import Optional
from pydantic import BaseModel, Json


class ValueType(str, Enum):

    binary = 'binary'
    bool = 'bool'
    float = 'float'
    int = 'int'
    str = 'str'
    

class Source(str, Enum):

    mrepresentationa = 'mrepresentationa'
    skema = 'skema'
    

class Format(str, Enum):

    bilayer = 'bilayer'
    gromet = 'gromet'
    other = 'other'
    sbml = 'sbml'
    

class OperationType(str, Enum):

    add = 'add'
    composition = 'composition'
    decomposition = 'decomposition'
    edit = 'edit'
    glue = 'glue'
    init = 'init'
    other = 'other'
    product = 'product'
    remove = 'remove'
    

class Direction(str, Enum):

    input = 'input'
    output = 'output'
    

class ExtractedType(str, Enum):

    equation = 'equation'
    figure = 'figure'
    table = 'table'
    

class TaggableTable(str, Enum):

    dataset = 'dataset'
    feature = 'feature'
    model = 'model'
    plan = 'plan'
    project = 'project'
    

class Importance(str, Enum):

    other = 'other'
    primary = 'primary'
    secondary = 'secondary'
    

class ObjType(str, Enum):

    dataset = 'dataset'
    model = 'model'
    plan = 'plan'
    project = 'project'
    representation = 'representation'
    runtime = 'runtime'
    software = 'software'
    

class RelationType(str, Enum):

    copies = 'copies'
    derives = 'derives'
    glued = 'glued'
    parents = 'parents'
    

class ResourceType(str, Enum):

    dataset = 'dataset'
    extracted_data = 'extracted_data'
    model = 'model'
    plan = 'plan'
    publication = 'publication'
    representation = 'representation'
    

class Role(str, Enum):

    author = 'author'
    contributor = 'contributor'
    maintainer = 'maintainer'
    other = 'other'
    

class Dataset(BaseModel):

    id: int
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


class Feature(BaseModel):

    id: int
    dataset_id: int
    description: Optional[str]
    display_name: Optional[str]
    name: str
    value_type: ValueType


class Qualifier(BaseModel):

    id: int
    dataset_id: int
    description: Optional[str]
    name: str
    value_type: ValueType


class QualifierXref(BaseModel):

    id: int
    qualifier_id: int
    feature_id: int


class Model(BaseModel):

    id: int
    created_at: datetime.datetime = datetime.datetime.now()
    name: str
    description: Optional[str]
    head_id: int


class Framework(BaseModel):

    id: int
    version: str
    name: str
    semantics: Json


class Operation(BaseModel):

    id: int
    prev: Optional[int]
    framework_id: int
    operation_type: OperationType
    model_content: Json
    timestamp: datetime.datetime = datetime.datetime.now()
    user: int


class Intermediate(BaseModel):

    id: int
    created_at: datetime.datetime
    source: Source
    type: Format
    representation: str
    model_id: Optional[int]
    software_id: Optional[int]


class Software(BaseModel):

    id: int
    timestamp: datetime.datetime = datetime.datetime.now()
    source: str
    storage_uri: str


class Runtime(BaseModel):

    id: int
    created_at: datetime.datetime = datetime.datetime.now()
    name: str
    left: int
    right: int


class Plan(BaseModel):

    id: int
    simulator: str
    query: str
    body: Json


class AppliedModel(BaseModel):

    id: int
    model_id: int
    plan_id: int


class Run(BaseModel):

    id: int
    simulator_id: int
    created_at: datetime.datetime = datetime.datetime.now()
    completed_at: Optional[datetime.datetime]
    success: Optional[bool] = True
    response: Optional[str]


class Material(BaseModel):

    id: int
    run_id: int
    dataset_id: int
    type: Optional[Direction]


class Parameter(BaseModel):

    id: int
    run_id: int
    name: str
    value: str
    value_type: str


class Publication(BaseModel):

    id: int
    xdd_uri: str


class ExtractedData(BaseModel):

    id: int
    publication_id: int
    type: ExtractedType
    data: str
    img: str


class Project(BaseModel):

    id: int
    name: str
    description: str
    timestamp: Optional[datetime.datetime] = datetime.datetime.now()
    status: str


class Asset(BaseModel):

    id: int
    project_id: int
    resource_id: int
    resource_type: ResourceType
    external_ref: Optional[str]


class Concept(BaseModel):

    id: int
    term_id: str
    type: TaggableTable
    obj_id: int
    status: Importance


class Relation(BaseModel):

    id: int
    created_at: datetime.datetime = datetime.datetime.now()
    relation_type: RelationType
    left: int
    left_type: ObjType
    right: int
    right_type: ObjType


class Person(BaseModel):

    id: int
    name: str
    email: str
    org: Optional[str]
    website: Optional[str]
    is_registered: bool


class Association(BaseModel):

    id: int
    person_id: int
    resource_id: int
    resource_type: Optional[ResourceType]
    role: Optional[Role]
