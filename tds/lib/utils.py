"""
TDS Utilities.
"""

import typing

from pydantic import BaseModel

_PATCHABLE_MODELS: typing.Dict[BaseModel, BaseModel] = {}


def patchable(model: BaseModel) -> BaseModel:
    """
    Create a fully optional version of a model for use with PATCH
    """
    model_name = f"Patchable{model.__name__}"
    if model_name in _PATCHABLE_MODELS:
        return _PATCHABLE_MODELS[model_name]

    PatchableModel = type(model_name, (model,), {})  # pylint: disable=invalid-name

    # Update the fields to be optional
    for field_def in PatchableModel.__fields__.values():
        field_def.required = False

    _PATCHABLE_MODELS[model_name] = PatchableModel
    return PatchableModel


def get_singular_index(index_str: str):
    """
    Function strips the s off of an index str.
    """
    if index_str[-1] == "s":
        return index_str.rstrip(index_str[-1])
    return index_str
