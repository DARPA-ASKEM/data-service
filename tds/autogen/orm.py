# pylint: skip-file
"""
ORM file from DBML autogen.
Skipping linter to prevent class docstring errors.
@TODO: Clean up file to pass linting.
"""
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from tds.autogen.enums import ExtractedType, ValueType

Base = declarative_base()


class QualifierXref(Base):
    __tablename__ = "qualifier_xref"

    id = sa.Column(sa.Integer(), primary_key=True)
    qualifier_id = sa.Column(
        sa.Integer(), sa.ForeignKey("qualifier.id"), nullable=False
    )
    feature_id = sa.Column(sa.Integer(), sa.ForeignKey("feature.id"), nullable=False)


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


class Extraction(Base):
    __tablename__ = "extraction"

    id = sa.Column(sa.Integer(), primary_key=True)
    publication_id = sa.Column(
        sa.Integer(), sa.ForeignKey("publication.id"), nullable=False
    )
    type = sa.Column(sa.Enum(ExtractedType), nullable=False)
    data = sa.Column(sa.LargeBinary(), nullable=False)
    img = sa.Column(sa.LargeBinary(), nullable=False)


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
