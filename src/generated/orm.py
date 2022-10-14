import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON


Base = declarative_base()


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
    

class Datasets(Base):

    __tablename__ = 'datasets'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    url = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    deprecated = sa.Column(sa.Boolean())
    sensitivity = sa.Column(sa.String())
    quality = sa.Column(sa.String())
    temporal_resolution = sa.Column(sa.String())
    geospatial_resolution = sa.Column(sa.String())


class Features(Base):

    __tablename__ = 'features'

    id = sa.Column(sa.Integer(), primary_key=True)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey('datasets.id'), nullable=False)
    feature = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.Enum(ValueType), nullable=False)
    value = sa.Column(sa.String(), nullable=False)


class Qualifiers(Base):

    __tablename__ = 'qualifiers'

    id = sa.Column(sa.Integer(), primary_key=True)
    qualifier_id = sa.Column(sa.Integer(), sa.ForeignKey('features.id'), nullable=False)
    qualified_id = sa.Column(sa.Integer(), sa.ForeignKey('features.id'), nullable=False)


class Models(Base):

    __tablename__ = 'models'

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String())
    head = sa.Column(sa.Integer(), sa.ForeignKey('operations.id'), nullable=False)


class Frameworks(Base):

    __tablename__ = 'frameworks'

    id = sa.Column(sa.Integer(), primary_key=True)
    runtime_id = sa.Column(sa.Integer(), sa.ForeignKey('runtimes.id'), nullable=False)
    version = sa.Column(sa.String(), nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    semantics = sa.Column(JSON(), nullable=False)


class Operations(Base):

    __tablename__ = 'operations'

    id = sa.Column(sa.Integer(), primary_key=True)
    prev = sa.Column(sa.Integer(), sa.ForeignKey('operations.id'), nullable=False)
    framework_id = sa.Column(sa.Integer(), sa.ForeignKey('frameworks.id'), nullable=False)
    operation_type = sa.Column(sa.Enum(Operation), nullable=False)
    model_content = sa.Column(JSON(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    user = sa.Column(sa.Integer(), sa.ForeignKey('people.id'), nullable=False)


class Representations(Base):

    __tablename__ = 'representations'

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), nullable=False)
    source = sa.Column(sa.Enum(Source), nullable=False)
    type = sa.Column(sa.Enum(Format), nullable=False)
    representation = sa.Column(sa.String(), nullable=False)
    model_id = sa.Column(sa.Integer(), sa.ForeignKey('models.id'), nullable=False)
    software_id = sa.Column(sa.Integer(), sa.ForeignKey('software.id'), nullable=False)


class Software(Base):

    __tablename__ = 'software'

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), nullable=False)
    source = sa.Column(sa.String(), nullable=False)
    storage_uri = sa.Column(sa.String(), nullable=False)


class Runtimes(Base):

    __tablename__ = 'runtimes'

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    name = sa.Column(sa.String(), nullable=False)
    left = sa.Column(sa.String(), nullable=False)
    right = sa.Column(sa.String(), nullable=False)


class Plans(Base):

    __tablename__ = 'plans'

    id = sa.Column(sa.Integer(), primary_key=True)
    simulator = sa.Column(sa.String(), nullable=False)
    query = sa.Column(sa.String(), nullable=False)
    body = sa.Column(sa.String(), nullable=False)


class AppliedModels(Base):

    __tablename__ = 'applied_models'

    id = sa.Column(sa.Integer(), primary_key=True)
    model_id = sa.Column(sa.Integer(), sa.ForeignKey('models.id'), nullable=False)
    plan_id = sa.Column(sa.Integer(), sa.ForeignKey('plans.id'), nullable=False)


class Runs(Base):

    __tablename__ = 'runs'

    id = sa.Column(sa.Integer(), primary_key=True)
    simulator_id = sa.Column(sa.Integer(), sa.ForeignKey('plans.id'), nullable=False)
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    completed_at = sa.Column(sa.DateTime())
    success = sa.Column(sa.Boolean(), server_default='True')
    response = sa.Column(sa.String())


class Materials(Base):

    __tablename__ = 'materials'

    id = sa.Column(sa.Integer(), primary_key=True)
    run_id = sa.Column(sa.Integer(), sa.ForeignKey('runs.id'), nullable=False)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey('datasets.id'), nullable=False)
    type = sa.Column(sa.Enum(Direction))


class Parameters(Base):

    __tablename__ = 'parameters'

    id = sa.Column(sa.Integer(), primary_key=True)
    run_id = sa.Column(sa.Integer(), sa.ForeignKey('runs.id'), nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    value = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.String(), nullable=False)


class Publications(Base):

    __tablename__ = 'publications'

    id = sa.Column(sa.Integer(), primary_key=True)
    xdd_uri = sa.Column(sa.String(), nullable=False)


class ExtractedData(Base):

    __tablename__ = 'extracted_data'

    id = sa.Column(sa.Integer(), primary_key=True)
    publication_id = sa.Column(sa.Integer(), sa.ForeignKey('publications.id'), nullable=False)
    type = sa.Column(sa.Enum(ExtractedType), nullable=False)
    data = sa.Column(sa.String(), nullable=False)
    img = sa.Column(sa.String(), nullable=False)


class Meta(Base):

    __tablename__ = 'meta'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), server_default=func.now())
    status = sa.Column(sa.String(), nullable=False)


class Assets(Base):

    __tablename__ = 'assets'

    id = sa.Column(sa.Integer(), primary_key=True)
    project_id = sa.Column(sa.Integer(), sa.ForeignKey('meta.id'), nullable=False)
    asset_id = sa.Column(sa.Integer(), sa.ForeignKey('models.id'), nullable=False)
    type = sa.Column(sa.Enum(AssetType), nullable=False)
    external_ref = sa.Column(sa.String())


class Associations(Base):

    __tablename__ = 'associations'

    id = sa.Column(sa.Integer(), primary_key=True)
    person_id = sa.Column(sa.Integer(), sa.ForeignKey('people.id'), nullable=False)
    asset_id = sa.Column(sa.Integer(), sa.ForeignKey('assets.id'), nullable=False)
    type = sa.Column(sa.Enum(AssetType))
    role = sa.Column(sa.Enum(Role))


class Concepts(Base):

    __tablename__ = 'concepts'

    id = sa.Column(sa.Integer(), primary_key=True)
    term_id = sa.Column(sa.String(), nullable=False)
    type = sa.Column(sa.Enum(TaggableType), nullable=False)
    obj_id = sa.Column(sa.Integer(), sa.ForeignKey('datasets.id'), nullable=False)
    status = sa.Column(sa.Enum(Importance), nullable=False)


class Relations(Base):

    __tablename__ = 'relations'

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    relation_type = sa.Column(sa.Enum(RelationType), nullable=False)
    left = sa.Column(sa.Integer(), sa.ForeignKey('meta.id'), nullable=False)
    left_type = sa.Column(sa.Enum(ObjType), nullable=False)
    right = sa.Column(sa.Integer(), sa.ForeignKey('meta.id'), nullable=False)
    right_type = sa.Column(sa.Enum(ObjType), nullable=False)


class People(Base):

    __tablename__ = 'people'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    email = sa.Column(sa.String(), nullable=False)
    org = sa.Column(sa.String(), nullable=False)
    website = sa.Column(sa.String(), nullable=False)
    is_registered = sa.Column(sa.Boolean(), nullable=False)
