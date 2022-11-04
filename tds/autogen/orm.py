import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON


Base = declarative_base()


class ResourceType(str, Enum):

    dataset = 'dataset'
    extracted_data = 'extracted_data'
    intermediate = 'intermediate'
    model = 'model'
    plan = 'plan'
    publication = 'publication'
    

class RelationType(str, Enum):

    cites = 'cites'
    copiedfrom = 'copiedfrom'
    derivedfrom = 'derivedfrom'
    editedFrom = 'editedFrom'
    gluedFrom = 'gluedFrom'
    stratifiedFrom = 'stratifiedFrom'
    

class TaggableType(str, Enum):

    dataset = 'dataset'
    feature = 'feature'
    model = 'model'
    project = 'project'
    simulation_plan = 'simulation_plan'
    

class FeatureValueType(str, Enum):

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
    

class QualifierXref(Base):

    __tablename__ = 'qualifier_xref'

    id = sa.Column(sa.Integer(), primary_key=True)
    qualifier_id = sa.Column(sa.Integer(), sa.ForeignKey('qualifier.id'), nullable=False)
    feature_id = sa.Column(sa.Integer(), sa.ForeignKey('feature.id'), nullable=False)


class ModelRuntime(Base):

    __tablename__ = 'model_runtime'

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    name = sa.Column(sa.String(), nullable=False)
    left = sa.Column(sa.Integer(), sa.ForeignKey('modeling_framework.id'), nullable=False)
    right = sa.Column(sa.Integer(), sa.ForeignKey('modeling_framework.id'), nullable=False)


class AppliedModel(Base):

    __tablename__ = 'applied_model'

    id = sa.Column(sa.Integer(), primary_key=True)
    model_id = sa.Column(sa.Integer(), sa.ForeignKey('model.id'), nullable=False)
    plan_id = sa.Column(sa.Integer(), sa.ForeignKey('simulation_plan.id'), nullable=False)


class SimulationMaterial(Base):

    __tablename__ = 'simulation_material'

    id = sa.Column(sa.Integer(), primary_key=True)
    run_id = sa.Column(sa.Integer(), sa.ForeignKey('simulation_run.id'), nullable=False)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey('dataset.id'), nullable=False)
    type = sa.Column(sa.Enum(Direction))


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
    maintainer = sa.Column(sa.Integer(), sa.ForeignKey('person.id'), nullable=False)


class Feature(Base):

    __tablename__ = 'feature'

    id = sa.Column(sa.Integer(), primary_key=True)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey('dataset.id'), nullable=False)
    description = sa.Column(sa.Text())
    display_name = sa.Column(sa.String())
    name = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.Enum(FeatureValueType), nullable=False)


class Qualifier(Base):

    __tablename__ = 'qualifier'

    id = sa.Column(sa.Integer(), primary_key=True)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey('dataset.id'), nullable=False)
    description = sa.Column(sa.Text())
    name = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.Enum(FeatureValueType), nullable=False)


class Model(Base):

    __tablename__ = 'model'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.Text())
    framework_id = sa.Column(sa.Integer(), sa.ForeignKey('modeling_framework.id'), nullable=False)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    content = sa.Column(JSON())


class SimulationRun(Base):

    __tablename__ = 'simulation_run'

    id = sa.Column(sa.Integer(), primary_key=True)
    simulator_id = sa.Column(sa.Integer(), sa.ForeignKey('simulation_plan.id'), nullable=False)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    completed_at = sa.Column(sa.DateTime())
    success = sa.Column(sa.Boolean(), server_default='True')
    response = sa.Column(sa.LargeBinary())


class ModelParameter(Base):

    __tablename__ = 'model_parameter'

    id = sa.Column(sa.Integer(), primary_key=True)
    run_id = sa.Column(sa.Integer(), sa.ForeignKey('simulation_run.id'), nullable=False)
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


class ProjectAsset(Base):

    __tablename__ = 'project_asset'

    id = sa.Column(sa.Integer(), primary_key=True)
    project_id = sa.Column(sa.Integer(), sa.ForeignKey('project.id'), nullable=False)
    resource_id = sa.Column(sa.Integer(), nullable=False)
    resource_type = sa.Column(sa.Enum(ResourceType), nullable=False)
    external_ref = sa.Column(sa.String())


class Provenance(Base):

    __tablename__ = 'provenance'

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    relation_type = sa.Column(sa.Enum(RelationType), nullable=False)
    left = sa.Column(sa.Integer(), nullable=False)
    left_type = sa.Column(sa.Enum(ResourceType), nullable=False)
    right = sa.Column(sa.Integer(), nullable=False)
    right_type = sa.Column(sa.Enum(ResourceType), nullable=False)
    user_id = sa.Column(sa.Integer(), sa.ForeignKey('person.id'))


class Association(Base):

    __tablename__ = 'association'

    id = sa.Column(sa.Integer(), primary_key=True)
    person_id = sa.Column(sa.Integer(), sa.ForeignKey('person.id'), nullable=False)
    resource_id = sa.Column(sa.Integer(), nullable=False)
    resource_type = sa.Column(sa.Enum(ResourceType))
    role = sa.Column(sa.Enum(Role))


class ModelingFramework(Base):

    __tablename__ = 'modeling_framework'

    id = sa.Column(sa.Integer(), primary_key=True)
    version = sa.Column(sa.String(), nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    semantics = sa.Column(JSON(), nullable=False)


class Intermediate(Base):

    __tablename__ = 'intermediate'

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    source = sa.Column(sa.Enum(IntermediateSource), nullable=False)
    type = sa.Column(sa.Enum(IntermediateFormat), nullable=False)
    representation = sa.Column(sa.LargeBinary(), nullable=False)


class Software(Base):

    __tablename__ = 'software'

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    source = sa.Column(sa.String(), nullable=False)
    storage_uri = sa.Column(sa.String(), nullable=False)


class SimulationPlan(Base):

    __tablename__ = 'simulation_plan'

    id = sa.Column(sa.Integer(), primary_key=True)
    simulator = sa.Column(sa.String(), nullable=False)
    query = sa.Column(sa.String(), nullable=False)
    body = sa.Column(JSON(), nullable=False)


class Publication(Base):

    __tablename__ = 'publication'

    id = sa.Column(sa.Integer(), primary_key=True)
    xdd_uri = sa.Column(sa.String(), nullable=False)


class Project(Base):

    __tablename__ = 'project'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), server_default=func.now())
    status = sa.Column(sa.String(), nullable=False)


class OntologyConcept(Base):

    __tablename__ = 'ontology_concept'

    id = sa.Column(sa.Integer(), primary_key=True)
    term_id = sa.Column(sa.String(), nullable=False)
    type = sa.Column(sa.Enum(TaggableType), nullable=False)
    obj_id = sa.Column(sa.Integer(), nullable=False)
    status = sa.Column(sa.Enum(OntologicalField), nullable=False)


class Person(Base):

    __tablename__ = 'person'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    email = sa.Column(sa.String(), nullable=False)
    org = sa.Column(sa.String())
    website = sa.Column(sa.String())
    is_registered = sa.Column(sa.Boolean(), nullable=False)
