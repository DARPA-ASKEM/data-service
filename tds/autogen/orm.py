import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON


Base = declarative_base()


class ResourceType(str, Enum):

    datasets = 'datasets'
    intermediates = 'intermediates'
    models = 'models'
    plans = 'plans'
    publications = 'publications'
    simulation_runs = 'simulation_runs'
    

class ProvenanceType(str, Enum):

    dataset = 'dataset'
    intermediate = 'intermediate'
    model = 'model'
    model_revision = 'model_revision'
    plan = 'plan'
    publication = 'publication'
    simulation_run = 'simulation_run'
    

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
    

class QualifierXref(Base):

    __tablename__ = 'qualifier_xref'

    id = sa.Column(sa.Integer(), primary_key=True)
    qualifier_id = sa.Column(sa.Integer(), sa.ForeignKey('qualifier.id'), nullable=False)
    feature_id = sa.Column(sa.Integer(), sa.ForeignKey('feature.id'), nullable=False)


class ModelDescription(Base):

    __tablename__ = 'model_description'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.Text())
    framework = sa.Column(sa.String(), sa.ForeignKey('model_framework.name'), nullable=False)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    state_id = sa.Column(sa.Integer(), sa.ForeignKey('model_state.id'), nullable=False)


class ModelRuntime(Base):

    __tablename__ = 'model_runtime'

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    name = sa.Column(sa.String(), nullable=False)
    left = sa.Column(sa.String(), sa.ForeignKey('model_framework.name'), nullable=False)
    right = sa.Column(sa.String(), sa.ForeignKey('model_framework.name'), nullable=False)


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
    annotations = sa.Column(JSON())
    maintainer = sa.Column(sa.Integer(), sa.ForeignKey('person.id'), nullable=False)
    simulation_run = sa.Column(sa.Boolean(), server_default='False')


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


class SimulationPlan(Base):

    __tablename__ = 'simulation_plan'

    id = sa.Column(sa.Integer(), primary_key=True)
    model_id = sa.Column(sa.Integer(), sa.ForeignKey('model_description.id'), nullable=False)
    simulator = sa.Column(sa.String(), nullable=False)
    query = sa.Column(sa.String(), nullable=False)
    content = sa.Column(JSON(), nullable=False)


class SimulationRun(Base):

    __tablename__ = 'simulation_run'

    id = sa.Column(sa.Integer(), primary_key=True)
    simulator_id = sa.Column(sa.Integer(), sa.ForeignKey('simulation_plan.id'), nullable=False)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    completed_at = sa.Column(sa.DateTime())
    success = sa.Column(sa.Boolean())
    dataset_id = sa.Column(sa.Integer())
    description = sa.Column(sa.Text())
    response = sa.Column(sa.LargeBinary())


class ModelParameter(Base):

    __tablename__ = 'model_parameter'

    id = sa.Column(sa.Integer(), primary_key=True)
    model_id = sa.Column(sa.Integer(), sa.ForeignKey('model_description.id'), nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    type = sa.Column(sa.Enum(ValueType), nullable=False)
    default_value = sa.Column(sa.String())
    state_variable = sa.Column(sa.Boolean(), nullable=False)


class SimulationParameter(Base):

    __tablename__ = 'simulation_parameter'

    id = sa.Column(sa.Integer(), primary_key=True)
    run_id = sa.Column(sa.Integer(), sa.ForeignKey('simulation_run.id'), nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    value = sa.Column(sa.String(), nullable=False)
    type = sa.Column(sa.Enum(ValueType), nullable=False)


class Extraction(Base):

    __tablename__ = 'extraction'

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


class OntologyConcept(Base):

    __tablename__ = 'ontology_concept'

    id = sa.Column(sa.Integer(), primary_key=True)
    curie = sa.Column(sa.String(), sa.ForeignKey('active_concept.curie'), nullable=False)
    type = sa.Column(sa.Enum(TaggableType), nullable=False)
    object_id = sa.Column(sa.Integer(), nullable=False)
    status = sa.Column(sa.Enum(OntologicalField), nullable=False)


class Provenance(Base):

    __tablename__ = 'provenance'

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    relation_type = sa.Column(sa.Enum(RelationType), nullable=False)
    left = sa.Column(sa.Integer(), nullable=False)
    left_type = sa.Column(sa.Enum(ProvenanceType), nullable=False)
    right = sa.Column(sa.Integer(), nullable=False)
    right_type = sa.Column(sa.Enum(ProvenanceType), nullable=False)
    user_id = sa.Column(sa.Integer(), sa.ForeignKey('person.id'))


class Association(Base):

    __tablename__ = 'association'

    id = sa.Column(sa.Integer(), primary_key=True)
    person_id = sa.Column(sa.Integer(), sa.ForeignKey('person.id'), nullable=False)
    resource_id = sa.Column(sa.Integer(), nullable=False)
    resource_type = sa.Column(sa.Enum(ResourceType))
    role = sa.Column(sa.Enum(Role))


class ModelFramework(Base):

    __tablename__ = 'model_framework'

    name = sa.Column(sa.String(), primary_key=True)
    version = sa.Column(sa.String(), nullable=False)
    semantics = sa.Column(sa.String(), nullable=False)


class ModelState(Base):

    __tablename__ = 'model_state'

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    content = sa.Column(JSON())


class Intermediate(Base):

    __tablename__ = 'intermediate'

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    source = sa.Column(sa.Enum(IntermediateSource), nullable=False)
    type = sa.Column(sa.Enum(IntermediateFormat), nullable=False)
    content = sa.Column(sa.LargeBinary(), nullable=False)


class Software(Base):

    __tablename__ = 'software'

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    source = sa.Column(sa.String(), nullable=False)
    storage_uri = sa.Column(sa.String(), nullable=False)


class Publication(Base):

    __tablename__ = 'publication'

    id = sa.Column(sa.Integer(), primary_key=True)
    xdd_uri = sa.Column(sa.String(), nullable=False)
    title = sa.Column(sa.String(), nullable=False)


class Project(Base):

    __tablename__ = 'project'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), server_default=func.now())
    active = sa.Column(sa.Boolean(), nullable=False)


class Person(Base):

    __tablename__ = 'person'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    email = sa.Column(sa.String(), nullable=False)
    org = sa.Column(sa.String())
    website = sa.Column(sa.String())
    is_registered = sa.Column(sa.Boolean(), nullable=False)


class ActiveConcept(Base):

    __tablename__ = 'active_concept'

    curie = sa.Column(sa.String(), primary_key=True)
    name = sa.Column(sa.String())
