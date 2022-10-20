"""
validation - does nothing yet
"""

from pydantic import BaseModel, Extra
from generated import schema
from typing import List


class PatchObj(BaseModel):
    class Config:
        extra = Extra.allow


class Concept(BaseModel):
    term_id : str
    status : schema.Importance


class Qualifier(schema.Qualifier):
    feature_names : List[str]
    concept : Concept


class Feature(schema.Feature):
    concept : Concept


class Dataset(schema.Dataset):
    features : List[Feature]
    qualifiers : List[Qualifier]
    concept : Concept


class ModelBody(schema.Operation):
    framework_name: str
    
    

class Model(schema.Model):
    body : ModelBody


"""
class Association(BaseModel):
    person : schema.Person
    role : schema.Role

class Project(schema.Meta):
    users : schema.Association
    assets : List[schema.Asset]
"""

