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


class ModelFramework(Base):
    __tablename__ = "model_framework"

    name = sa.Column(sa.String(), primary_key=True)
    version = sa.Column(sa.String(), nullable=False)
    semantics = sa.Column(sa.String(), nullable=False)
    schema_url = sa.Column(sa.String())
