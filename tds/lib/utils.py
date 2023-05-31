import copy
from typing import Type

from pydantic import BaseModel


def patchable(model: BaseModel) -> BaseModel:
    """
    Create a fully optional version of a model for use with PATCH
    """
    patchabel_model = copy.deepcopy(model)
    for field_def in patchabel_model.__fields__.values():
        field_def.required = False
    return patchabel_model
