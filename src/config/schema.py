"""
api_schema - Provides the API interface with the data store contents.
"""

from json import dumps
from pydantic import BaseModel
from generated import schema, orm
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

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, body : orm.Operation) -> 'ModelBody':
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        setattr(body, 'model_content', dumps(body.model_content))
        return super().from_orm(body)


class Model(schema.Model):
    body : ModelBody
    concept : Optional[Concept]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, metadata : orm.Model, body : orm.Operation) -> 'Model':
        """
        Handle ORM conversion with insertion of model body into schema
        """
        model_body = ModelBody.from_orm(body)
        setattr(metadata, 'body', model_body)
        return super().from_orm(metadata)
        

"""
class Association(BaseModel):
    person : schema.Person
    role : schema.Role

class Project(schema.Meta):
    users : schema.Association
    assets : List[schema.Asset]
"""

