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
