# pylint: skip-file
"""
ORM file from DBML autogen.
Skipping linter to prevent class docstring errors.
@TODO: Clean up file to pass linting.
"""
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from tds.db.enums import ValueType

Base = declarative_base()


class Feature(Base):
    __tablename__ = "feature"

    id = sa.Column(sa.Integer(), primary_key=True)
    dataset_id = sa.Column(sa.Integer(), sa.ForeignKey("dataset.id"), nullable=False)
    description = sa.Column(sa.Text())
    display_name = sa.Column(sa.String())
    name = sa.Column(sa.String(), nullable=False)
    value_type = sa.Column(sa.Enum(ValueType), nullable=False)
