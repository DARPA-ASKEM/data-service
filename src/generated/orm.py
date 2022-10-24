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
    

class Operation(Base):

    __tablename__ = 'operation'

    id = sa.Column(sa.Integer(), primary_key=True)
    prev = sa.Column(sa.Integer(), sa.ForeignKey('operation.id'))
    framework_id = sa.Column(sa.Integer(), sa.ForeignKey('framework.id'), nullable=False)
    operation_type = sa.Column(sa.Enum(OperationType), nullable=False)
    model_content = sa.Column(JSON(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    user = sa.Column(sa.Integer(), sa.ForeignKey('person.id'), nullable=False)


class QualifierXref(Base):

    __tablename__ = 'qualifier_xref'

    id = sa.Column(sa.Integer(), primary_key=True)
    qualifier_id = sa.Column(sa.Integer(), sa.ForeignKey('qualifier.id'), nullable=False)
    feature_id = sa.Column(sa.Integer(), sa.ForeignKey('feature.id'), nullable=False)


class Intermediate(Base):

    __tablename__ = 'intermediate'

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), nullable=False)
    source = sa.Column(sa.Enum(Source), nullable=False)
    type = sa.Column(sa.Enum(Format), nullable=False)
    representation = sa.Column(sa.LargeBinary(), nullable=False)
    model_id = sa.Column(sa.Integer(), sa.ForeignKey('model.id'))
    software_id = sa.Column(sa.Integer(), sa.ForeignKey('software.id'))


class Runtime(Base):

    __tablename__ = 'runtime'

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    name = sa.Column(sa.String(), nullable=False)
    left = sa.Column(sa.Integer(), sa.ForeignKey('framework.id'), nullable=False)
    right = sa.Column(sa.Integer(), sa.ForeignKey('framework.id'), nullable=False)


class AppliedModel(Base):

    __tablename__ = 'applied_model'

    id = sa.Column(sa.Integer(), primary_key=True)
    model_id = sa.Column(sa.Integer(), sa.ForeignKey('model.id'), nullable=False)
    plan_id = sa.Column(sa.Integer(), sa.ForeignKey('plan.id'), nullable=False)


class Material(Base):

    __tablename__ = 'material'

    id = sa.Column(sa.Integer(), primary_key=True)
    run_id = sa.Column(sa.Integer(), sa.ForeignKey('run.id'), nullable=False)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey('dataset.id'), nullable=False)
    type = sa.Column(sa.Enum(Direction))


class Association(Base):

    __tablename__ = 'association'

    id = sa.Column(sa.Integer(), primary_key=True)
    person_id = sa.Column(sa.Integer(), sa.ForeignKey('person.id'), nullable=False)
    asset_id = sa.Column(sa.Integer(), sa.ForeignKey('asset.id'), nullable=False)
    type = sa.Column(sa.Enum(AssetTable))
    role = sa.Column(sa.Enum(Role))


class Feature(Base):

    __tablename__ = 'feature'

    id = sa.Column(sa.Integer(), primary_key=True)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey('dataset.id'), nullable=False)
    description = sa.Column(sa.Text())
    display_name = sa.Column(sa.String())
    name = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.Enum(ValueType), nullable=False)


class Qualifier(Base):

    __tablename__ = 'qualifier'

    id = sa.Column(sa.Integer(), primary_key=True)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey('dataset.id'), nullable=False)
    description = sa.Column(sa.Text())
    name = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.Enum(ValueType), nullable=False)


class Model(Base):

    __tablename__ = 'model'

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.Text())
    head_id = sa.Column(sa.Integer(), sa.ForeignKey('operation.id'), nullable=False)


class Run(Base):

    __tablename__ = 'run'

    id = sa.Column(sa.Integer(), primary_key=True)
    simulator_id = sa.Column(sa.Integer(), sa.ForeignKey('plan.id'), nullable=False)
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    completed_at = sa.Column(sa.DateTime())
    success = sa.Column(sa.Boolean(), server_default='True')
    response = sa.Column(sa.LargeBinary())


class Parameter(Base):

    __tablename__ = 'parameter'

    id = sa.Column(sa.Integer(), primary_key=True)
    run_id = sa.Column(sa.Integer(), sa.ForeignKey('run.id'), nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    value = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.String(), nullable=False)


class ExtractedData(Base):

    __tablename__ = 'extracted_data'

    id = sa.Column(sa.Integer(), primary_key=True)
    publication_id = sa.Column(sa.Integer(), sa.ForeignKey('publication.id'), nullable=False)
    type = sa.Column(sa.Enum(ExtractedType), nullable=False)
    data = sa.Column(sa.LargeBinary(), nullable=False)
    img = sa.Column(sa.LargeBinary(), nullable=False)


class Asset(Base):

    __tablename__ = 'asset'

    id = sa.Column(sa.Integer(), primary_key=True)
    project_id = sa.Column(sa.Integer(), sa.ForeignKey('meta.id'), nullable=False)
    asset_id = sa.Column(sa.Integer(), nullable=False)
    type = sa.Column(sa.Enum(AssetTable), nullable=False)
    external_ref = sa.Column(sa.String())


class Dataset(Base):

    __tablename__ = 'dataset'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    url = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.Text(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    deprecated = sa.Column(sa.Boolean())
    sensitivity = sa.Column(sa.Text())
    quality = sa.Column(sa.Text())
    temporal_resolution = sa.Column(sa.String())
    geospatial_resolution = sa.Column(sa.String())


class Framework(Base):

    __tablename__ = 'framework'

    id = sa.Column(sa.Integer(), primary_key=True)
    version = sa.Column(sa.String(), nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    semantics = sa.Column(JSON(), nullable=False)


class Software(Base):

    __tablename__ = 'software'

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), nullable=False)
    source = sa.Column(sa.String(), nullable=False)
    storage_uri = sa.Column(sa.String(), nullable=False)


class Plan(Base):

    __tablename__ = 'plan'

    id = sa.Column(sa.Integer(), primary_key=True)
    simulator = sa.Column(sa.String(), nullable=False)
    query = sa.Column(sa.String(), nullable=False)
    body = sa.Column(JSON(), nullable=False)


class Publication(Base):

    __tablename__ = 'publication'

    id = sa.Column(sa.Integer(), primary_key=True)
    xdd_uri = sa.Column(sa.String(), nullable=False)


class Meta(Base):

    __tablename__ = 'meta'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), server_default=func.now())
    status = sa.Column(sa.String(), nullable=False)


class Concept(Base):

    __tablename__ = 'concept'

    id = sa.Column(sa.Integer(), primary_key=True)
    term_id = sa.Column(sa.String(), nullable=False)
    type = sa.Column(sa.Enum(TaggableTable), nullable=False)
    obj_id = sa.Column(sa.Integer(), nullable=False)
    status = sa.Column(sa.Enum(Importance), nullable=False)


class Relation(Base):

    __tablename__ = 'relation'

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    relation_type = sa.Column(sa.Enum(RelationType), nullable=False)
    left = sa.Column(sa.Integer(), nullable=False)
    left_type = sa.Column(sa.Enum(ObjType), nullable=False)
    right = sa.Column(sa.Integer(), nullable=False)
    right_type = sa.Column(sa.Enum(ObjType), nullable=False)


class Person(Base):

    __tablename__ = 'person'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    email = sa.Column(sa.String(), nullable=False)
    org = sa.Column(sa.String())
    website = sa.Column(sa.String())
    is_registered = sa.Column(sa.Boolean(), nullable=False)
