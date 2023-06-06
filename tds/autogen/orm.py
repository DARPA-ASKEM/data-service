# pylint: skip-file
"""
ORM file from DBML autogen.
Skipping linter to prevent class docstring errors.
@TODO: Clean up file to pass linting.
"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from tds.autogen.enums import (
    ExtractedType,
    ProvenanceType,
    RelationType,
    ResourceType,
    Role,
    ValueType,
)

Base = declarative_base()


class QualifierXref(Base):
    __tablename__ = "qualifier_xref"

    id = sa.Column(sa.Integer(), primary_key=True)
    qualifier_id = sa.Column(
        sa.Integer(), sa.ForeignKey("qualifier.id"), nullable=False
    )
    feature_id = sa.Column(sa.Integer(), sa.ForeignKey("feature.id"), nullable=False)


class ModelDescription(Base):
    __tablename__ = "model_description"

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.Text())
    framework = sa.Column(
        sa.String(), sa.ForeignKey("model_framework.name"), nullable=False
    )
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    state_id = sa.Column(sa.Integer(), sa.ForeignKey("model_state.id"), nullable=False)


class ModelRuntime(Base):
    __tablename__ = "model_runtime"

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    name = sa.Column(sa.String(), nullable=False)
    left = sa.Column(sa.String(), sa.ForeignKey("model_framework.name"), nullable=False)
    right = sa.Column(
        sa.String(), sa.ForeignKey("model_framework.name"), nullable=False
    )


class SimulationParameter(Base):
    __tablename__ = "simulation_parameter"

    id = sa.Column(sa.Integer(), primary_key=True)
    run_id = sa.Column(sa.Integer(), sa.ForeignKey("simulation_run.id"), nullable=False)
    model_parameter_id = sa.Column(sa.Integer(), sa.ForeignKey("model_parameter.id"))
    name = sa.Column(sa.String(), nullable=False)
    value = sa.Column(sa.String(), nullable=False)
    type = sa.Column(sa.Enum(ValueType), nullable=False)


class Dataset(Base):
    __tablename__ = "dataset"

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    url = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.Text(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    deprecated = sa.Column(sa.Boolean(), server_default="False")
    sensitivity = sa.Column(sa.Text())
    quality = sa.Column(sa.Text())
    temporal_resolution = sa.Column(sa.String())
    geospatial_resolution = sa.Column(sa.String())
    annotations = sa.Column(JSON())
    data_path = sa.Column(sa.String())
    maintainer = sa.Column(sa.Integer(), sa.ForeignKey("person.id"))
    simulation_run = sa.Column(sa.Boolean(), server_default="False")


class Feature(Base):
    __tablename__ = "feature"

    id = sa.Column(sa.Integer(), primary_key=True)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey("dataset.id"), nullable=False)
    description = sa.Column(sa.Text())
    display_name = sa.Column(sa.String())
    name = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.Enum(ValueType), nullable=False)


class Qualifier(Base):
    __tablename__ = "qualifier"

    id = sa.Column(sa.Integer(), primary_key=True)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey("dataset.id"), nullable=False)
    description = sa.Column(sa.Text())
    name = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.Enum(ValueType), nullable=False)


class SimulationRun(Base):
    __tablename__ = "simulation_run"

    id = sa.Column(sa.Integer(), primary_key=True)
    simulator_id = sa.Column(
        sa.Integer(), sa.ForeignKey("model_configuration.id"), nullable=False
    )
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    completed_at = sa.Column(sa.DateTime())
    success = sa.Column(sa.Boolean())
    dataset_id = sa.Column(sa.Integer())
    description = sa.Column(sa.Text())
    response = sa.Column(sa.LargeBinary())


class ModelParameter(Base):
    __tablename__ = "model_parameter"

    id = sa.Column(sa.Integer(), primary_key=True)
    model_id = sa.Column(sa.Integer(), sa.ForeignKey("model_description.id"))
    name = sa.Column(sa.String(), nullable=False)
    type = sa.Column(sa.Enum(ValueType), nullable=False)
    default_value = sa.Column(sa.String())
    state_variable = sa.Column(sa.Boolean(), nullable=False)


class Extraction(Base):
    __tablename__ = "extraction"

    id = sa.Column(sa.Integer(), primary_key=True)
    publication_id = sa.Column(
        sa.Integer(), sa.ForeignKey("publication.id"), nullable=False
    )
    type = sa.Column(sa.Enum(ExtractedType), nullable=False)
    data = sa.Column(sa.LargeBinary(), nullable=False)
    img = sa.Column(sa.LargeBinary(), nullable=False)


class ProjectAsset(Base):
    __tablename__ = "project_asset"

    id = sa.Column(sa.Integer(), primary_key=True)
    project_id = sa.Column(sa.Integer(), sa.ForeignKey("project.id"), nullable=False)
    resource_id = sa.Column(sa.String(), nullable=False)
    resource_type = sa.Column(sa.Enum(ResourceType), nullable=False)
    external_ref = sa.Column(sa.String())


class Provenance(Base):
    __tablename__ = "provenance"

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    relation_type = sa.Column(sa.Enum(RelationType), nullable=False)
    left = sa.Column(sa.String(), nullable=False)
    left_type = sa.Column(sa.Enum(ProvenanceType), nullable=False)
    right = sa.Column(sa.String(), nullable=False)
    right_type = sa.Column(sa.Enum(ProvenanceType), nullable=False)
    user_id = sa.Column(sa.Integer(), sa.ForeignKey("person.id"))
    concept = sa.Column(sa.String())


class Association(Base):
    __tablename__ = "association"

    id = sa.Column(sa.Integer(), primary_key=True)
    person_id = sa.Column(sa.Integer(), sa.ForeignKey("person.id"), nullable=False)
    resource_id = sa.Column(sa.Integer(), nullable=False)
    resource_type = sa.Column(sa.Enum(ResourceType))
    role = sa.Column(sa.Enum(Role))


class ModelFramework(Base):
    __tablename__ = "model_framework"

    name = sa.Column(sa.String(), primary_key=True)
    version = sa.Column(sa.String(), nullable=False)
    semantics = sa.Column(sa.String(), nullable=False)
    schema_url = sa.Column(sa.String())


class Software(Base):
    __tablename__ = "software"

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    source = sa.Column(sa.String(), nullable=False)
    storage_uri = sa.Column(sa.String(), nullable=False)


class Publication(Base):
    __tablename__ = "publication"

    id = sa.Column(sa.Integer(), primary_key=True)
    xdd_uri = sa.Column(sa.String(), nullable=False)
    title = sa.Column(sa.String(), nullable=False)


class Project(Base):
    __tablename__ = "project"

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)
    timestamp = sa.Column(sa.DateTime(), server_default=func.now())
    active = sa.Column(sa.Boolean(), nullable=False)
    username = sa.Column(sa.String())


class Person(Base):
    __tablename__ = "person"

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    email = sa.Column(sa.String(), nullable=False)
    org = sa.Column(sa.String())
    website = sa.Column(sa.String())
    is_registered = sa.Column(sa.Boolean(), nullable=False)
