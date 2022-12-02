"""
Scalar Schema
"""

from enum import Enum
from logging import Logger

import strawberry

from tds.autogen import schema

logger = Logger(__name__)


@strawberry.enum
class ValueType(Enum):
    binary = schema.ValueType.binary.name
    bool = schema.ValueType.bool.name
    float = schema.ValueType.float.name
    int = schema.ValueType.int.name
    str = schema.ValueType.str.name
