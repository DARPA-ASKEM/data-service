"""
Concept Schema
"""

# pylint: disable=missing-class-docstring, no-member, missing-function-docstring

from logging import Logger
from typing import List, Optional

import strawberry
from sqlalchemy.orm import Session
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import list_by_id
from tds.graphql.dataset import Dataset, Feature, Qualifier
from tds.graphql.enum import OntologicalField, TaggableType
from tds.graphql.helper import sqlalchemy_type
from tds.graphql.model import Intermediate, Model, ModelParameter
from tds.graphql.project import Project
from tds.graphql.publication import Publication
from tds.graphql.simulation import Plan, Run, RunParameter

logger = Logger(__name__)

orm_enum_to_type = {
    TaggableType.simulation_plans: Plan,
    TaggableType.models: Model,
    TaggableType.simulation_runs: Run,
    TaggableType.datasets: Dataset,
    TaggableType.intermediates: Intermediate,
    TaggableType.publications: Publication,
    TaggableType.projects: Project,
    TaggableType.simulation_parameters: RunParameter,
    TaggableType.model_parameters: ModelParameter,
    TaggableType.features: Feature,
    TaggableType.qualifiers: Qualifier,
}

Object = (
    Model
    | Plan
    | Run
    | Dataset
    | Intermediate
    | Publication
    | Project
    | RunParameter
    | Model
    | Feature
    | Qualifier
    | ModelParameter
)


class ConceptSchema(schema.OntologyConcept):
    class Config:
        orm_mode = True


@sqlalchemy_type(orm.OntologyConcept)
@strawberry.experimental.pydantic.type(model=ConceptSchema)
class Concept:

    id: strawberry.auto
    curie: strawberry.auto
    type: TaggableType
    object_id: strawberry.auto
    status: OntologicalField

    @strawberry.field
    def name(self, info: Info) -> Optional[str]:
        with Session(info.context["rdb"]) as session:
            return session.query(orm.ActiveConcept).get(self.curie).name

    @strawberry.field
    def object(self, info: Info) -> Object:
        with Session(info.context["rdb"]) as session:
            return orm_enum_to_type[self.type].fetch_from_sql(session, self.object_id)

    @staticmethod
    def from_pydantic(instance: ConceptSchema) -> "Concept":
        data = instance.dict()
        data["type"] = TaggableType(data["type"].name)
        data["status"] = OntologicalField(data["status"].name)
        return Concept(**data)


def list_concepts(info: Info, curies: Optional[List[str]] = None) -> List[Concept]:
    if curies is not None:
        with Session(info.context["rdb"]) as session:
            fetched_concepts = (
                session.query(orm.OntologyConcept)
                .filter(orm.OntologyConcept.curie.in_(curies))
                .all()
            )

    else:
        fetched_concepts: List[orm.Project] = list_by_id(
            info.context["rdb"].connect(), orm.OntologyConcept, 100, 0
        )
    return [Concept.from_orm(concept) for concept in fetched_concepts]
