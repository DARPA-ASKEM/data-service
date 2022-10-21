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
    

class AssetTable(str, Enum):

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


class QualifierXref(BaseModel):

    id: Optional[int] = None
    qualifier_id: Optional[int] = None
    feature_id: Optional[int] = None


class Model(BaseModel):

    id: Optional[int] = None
    created_at: datetime.datetime = datetime.datetime.now()
    name: str
    description: Optional[str]
    head_id: Optional[int] = None


class Framework(BaseModel):

    id: Optional[int] = None
    version: str
    name: str
    semantics: Json


class Operation(BaseModel):

    id: Optional[int] = None
    prev: Optional[int]
    framework_id: Optional[int] = None
    operation_type: OperationType
    model_content: Json
    timestamp: datetime.datetime = datetime.datetime.now()
    user: int


class Intermediate(BaseModel):

    id: Optional[int] = None
    created_at: datetime.datetime
    source: Source
    type: Format
    representation: bytes
    model_id: Optional[int]
    software_id: Optional[int]


class Software(BaseModel):

    id: Optional[int] = None
    created_at: datetime.datetime
    source: str
    storage_uri: str


class Runtime(BaseModel):

    id: Optional[int] = None
    created_at: datetime.datetime = datetime.datetime.now()
    name: str
    left: int
    right: int


class Plan(BaseModel):

    id: Optional[int] = None
    simulator: str
    query: str
    body: Json


class AppliedModel(BaseModel):

    id: Optional[int] = None
    model_id: Optional[int] = None
    plan_id: Optional[int] = None


class Run(BaseModel):

    id: Optional[int] = None
    simulator_id: Optional[int] = None
    created_at: datetime.datetime = datetime.datetime.now()
    completed_at: Optional[datetime.datetime]
    success: Optional[bool] = True
    response: Optional[bytes]


class Material(BaseModel):

    id: Optional[int] = None
    run_id: Optional[int] = None
    dataset_id: Optional[int] = None
    type: Optional[Direction]


class Parameter(BaseModel):

    id: Optional[int] = None
    run_id: Optional[int] = None
    name: str
    value: str
    value_type: str


class Publication(BaseModel):

    id: Optional[int] = None
    xdd_uri: str


class ExtractedData(BaseModel):

    id: Optional[int] = None
    publication_id: Optional[int] = None
    type: ExtractedType
    data: bytes
    img: bytes


class Meta(BaseModel):

    id: Optional[int] = None
    name: str
    description: str
    timestamp: Optional[datetime.datetime] = datetime.datetime.now()
    status: str


class Asset(BaseModel):

    id: Optional[int] = None
    project_id: Optional[int] = None
    asset_id: Optional[int] = None
    type: AssetTable
    external_ref: Optional[str]


class Association(BaseModel):

    id: Optional[int] = None
    person_id: Optional[int] = None
    asset_id: Optional[int] = None
    type: Optional[AssetTable]
    role: Optional[Role]


class Concept(BaseModel):

    id: Optional[int] = None
    term_id: str
    type: TaggableTable
    obj_id: Optional[int] = None
    status: Importance


class Relation(BaseModel):

    id: Optional[int] = None
    created_at: datetime.datetime = datetime.datetime.now()
    relation_type: RelationType
    left: int
    left_type: ObjType
    right: int
    right_type: ObjType


class Person(BaseModel):

    id: Optional[int] = None
    name: str
    email: str
    org: Optional[str]
    website: Optional[str]
    is_registered: bool
