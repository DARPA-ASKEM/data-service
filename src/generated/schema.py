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
    

class Operation(str, Enum):

    add = 'add'
    composition = 'composition'
    decomposition = 'decomposition'
    glue = 'glue'
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
    

class AssetType(str, Enum):

    dataset = 'dataset'
    extracted_data = 'extracted_data'
    model = 'model'
    publication = 'publication'
    representations = 'representations'
    simulator = 'simulator'
    

class Role(str, Enum):

    author = 'author'
    contributor = 'contributor'
    maintainer = 'maintainer'
    other = 'other'
    

class TaggableType(str, Enum):

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
    plans = 'plans'
    project = 'project'
    representations = 'representations'
    runtimes = 'runtimes'
    software = 'software'
    

class RelationType(str, Enum):

    copies = 'copies'
    derives = 'derives'
    glued = 'glued'
    parents = 'parents'
    

class Datasets(BaseModel):

    id: Optional[int] = None
    name: str
    url: str
    description: bytes
    timestamp: datetime.datetime = datetime.datetime.now()
    deprecated: Optional[bool]
    sensitivity: Optional[bytes]
    quality: Optional[bytes]
    temporal_resolution: Optional[str]
    geospatial_resolution: Optional[str]


class Features(BaseModel):

    id: Optional[int] = None
    dataset_id: Optional[int] = None
    feature: str
    value_type: ValueType
    value: str


class Qualifiers(BaseModel):

    id: Optional[int] = None
    qualifier_id: Optional[int] = None
    qualified_id: Optional[int] = None


class Models(BaseModel):

    id: Optional[int] = None
    created_at: datetime.datetime = datetime.datetime.now()
    name: str
    description: Optional[bytes]
    head: int


class Frameworks(BaseModel):

    id: Optional[int] = None
    runtime_id: Optional[int] = None
    version: str
    name: str
    semantics: Json


class Operations(BaseModel):

    id: Optional[int] = None
    prev: int
    framework_id: Optional[int] = None
    operation_type: Operation
    model_content: Json
    timestamp: datetime.datetime = datetime.datetime.now()
    user: int


class Representations(BaseModel):

    id: Optional[int] = None
    created_at: datetime.datetime
    source: Source
    type: Format
    representation: bytes
    model_id: Optional[int] = None
    software_id: Optional[int] = None


class Software(BaseModel):

    id: Optional[int] = None
    created_at: datetime.datetime
    source: str
    storage_uri: str


class Runtimes(BaseModel):

    id: Optional[int] = None
    created_at: datetime.datetime = datetime.datetime.now()
    name: str
    left: str
    right: str


class Plans(BaseModel):

    id: Optional[int] = None
    simulator: str
    query: str
    body: bytes


class AppliedModels(BaseModel):

    id: Optional[int] = None
    model_id: Optional[int] = None
    plan_id: Optional[int] = None


class Runs(BaseModel):

    id: Optional[int] = None
    simulator_id: Optional[int] = None
    created_at: datetime.datetime = datetime.datetime.now()
    completed_at: Optional[datetime.datetime]
    success: Optional[bool] = True
    response: Optional[bytes]


class Materials(BaseModel):

    id: Optional[int] = None
    run_id: Optional[int] = None
    dataset_id: Optional[int] = None
    type: Optional[Direction]


class Parameters(BaseModel):

    id: Optional[int] = None
    run_id: Optional[int] = None
    name: str
    value: str
    value_type: str


class Publications(BaseModel):

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


class Assets(BaseModel):

    id: Optional[int] = None
    project_id: Optional[int] = None
    asset_id: Optional[int] = None
    type: AssetType
    external_ref: Optional[str]


class Associations(BaseModel):

    id: Optional[int] = None
    person_id: Optional[int] = None
    asset_id: Optional[int] = None
    type: Optional[AssetType]
    role: Optional[Role]


class Concepts(BaseModel):

    id: Optional[int] = None
    term_id: str
    type: TaggableType
    obj_id: Optional[int] = None
    status: Importance


class Relations(BaseModel):

    id: Optional[int] = None
    created_at: datetime.datetime = datetime.datetime.now()
    relation_type: RelationType
    left: int
    left_type: ObjType
    right: int
    right_type: ObjType


class People(BaseModel):

    id: Optional[int] = None
    name: str
    email: str
    org: str
    website: str
    is_registered: bool
