"""
TDS Utilities.
"""

from pydantic import BaseModel


def patchable(model: BaseModel) -> BaseModel:
    """
    Create a fully optional version of a model for use with PATCH
    """

    # Create new class that inherits from passed in class
    class PatchableModel(model):
        ...

    # Update the fields to be optional
    for field_def in PatchableModel.__fields__.values():
        field_def.required = False
    return PatchableModel
