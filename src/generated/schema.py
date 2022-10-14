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


class Features(BaseModel):

    id: int
    dataset_id: int
    feature: str
    value_type: ValueType
    value: str


class Qualifiers(BaseModel):

    id: int
    qualifier_id: int
    qualified_id: int


class Models(BaseModel):

    id: int
    created_at: datetime.datetime = datetime.datetime.now()
    name: str
    description: Optional[str]
    head: int


class Frameworks(BaseModel):

    id: int
    runtime_id: int
    version: str
    name: str
    semantics: Json


class Operations(BaseModel):

    id: int
    prev: int
    framework_id: int
    operation_type: Operation
    model_content: Json
    timestamp: datetime.datetime = datetime.datetime.now()
    user: int


class Representations(BaseModel):

    id: int
    created_at: datetime.datetime
    source: Source
    type: Format
    representation: str
    model_id: int
    software_id: int


class Software(BaseModel):

    id: int
    created_at: datetime.datetime
    source: str
    storage_uri: str


class Runtimes(BaseModel):

    id: int
    created_at: datetime.datetime = datetime.datetime.now()
    name: str
    left: str
    right: str


class Plans(BaseModel):

    id: int
    simulator: str
    query: str
    body: str


class AppliedModels(BaseModel):

    id: int
    model_id: int
    plan_id: int


class Runs(BaseModel):

    id: int
    simulator_id: int
    created_at: datetime.datetime = datetime.datetime.now()
    completed_at: Optional[datetime.datetime]
    success: Optional[bool] = True
    response: Optional[str]


class Materials(BaseModel):

    id: int
    run_id: int
    dataset_id: int
    type: Optional[Direction]


class Parameters(BaseModel):

    id: int
    run_id: int
    name: str
    value: str
    value_type: str


class Publications(BaseModel):

    id: int
    xdd_uri: str


class ExtractedData(BaseModel):

    id: int
    publication_id: int
    type: ExtractedType
    data: str
    img: str


class Meta(BaseModel):

    id: int
    name: str
    description: str
    timestamp: Optional[datetime.datetime] = datetime.datetime.now()
    status: str


class Assets(BaseModel):

    id: int
    project_id: int
    asset_id: int
    type: AssetType
    external_ref: Optional[str]


class Associations(BaseModel):

    id: int
    person_id: int
    asset_id: int
    type: Optional[AssetType]
    role: Optional[Role]


class Concepts(BaseModel):

    id: int
    term_id: str
    type: TaggableType
    obj_id: int
    status: Importance


class Relations(BaseModel):

    id: int
    created_at: datetime.datetime = datetime.datetime.now()
    relation_type: RelationType
    left: int
    left_type: ObjType
    right: int
    right_type: ObjType


class People(BaseModel):

    id: int
    name: str
    email: str
    org: str
    website: str
    is_registered: bool
