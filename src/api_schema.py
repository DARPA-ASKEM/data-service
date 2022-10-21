"""
api_schema - does nothing yet
"""

from pydantic import BaseModel
from generated import schema
from typing import List, Optional


class Concept(BaseModel):
    term_id : str
    status : schema.Importance


class Qualifier(schema.Qualifier):
    feature_names : List[str]
    concept : Optional[Concept]


class Feature(schema.Feature):
    concept : Optional[Concept]


class Dataset(schema.Dataset):
    features : List[Feature]
    qualifiers : List[Qualifier]
    concept : Optional[Concept]


class ModelBody(schema.Operation):
    framework_id = 0 # TODO(five): Implement framework crud
    #framework_name : str = 'dummy' # TODO(five): Look up id using name
    user = 0 # TODO(five): Implement person crud


class Model(schema.Model):
    body : ModelBody
    concept : Optional[Concept]


"""
class Association(BaseModel):
    person : schema.Person
    role : schema.Role

class Project(schema.Meta):
    users : schema.Association
    assets : List[schema.Asset]
"""

