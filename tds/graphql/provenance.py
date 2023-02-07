"""
Concept Schema
"""

# pylint: disable=missing-class-docstring, no-member, missing-function-docstring

from logging import Logger
from typing import List, Optional

import strawberry
from sqlalchemy.orm import Session
from strawberry.types import Info

from tds.autogen.schema import ProvenanceType
from tds.db.graph.search_provenance import SearchProvenance
from tds.graphql.dataset import Dataset
from tds.graphql.model import Intermediate, Model, ModelParameter
from tds.graphql.project import Project
from tds.graphql.publication import Publication
from tds.graphql.simulation import Plan, Run, RunParameter
from tds.schema.provenance import NodeSchema

logger = Logger(__name__)

orm_enum_to_type = {
    ProvenanceType.Plan: Plan,
    ProvenanceType.Model: Model,
    ProvenanceType.SimulationRun: Run,
    ProvenanceType.Dataset: Dataset,
    ProvenanceType.Intermediate: Intermediate,
    ProvenanceType.Publication: Publication,
    ProvenanceType.Project: Project,
    ProvenanceType.PlanParameter: RunParameter,
    ProvenanceType.ModelParameter: ModelParameter,
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
    | ModelParameter
)


@strawberry.experimental.pydantic.type(model=NodeSchema)
class Provenance:
    id: strawberry.auto
    type: strawberry.auto
    uuid: strawberry.auto

    @strawberry.field
    def object(self, info: Info) -> Object:
        with Session(info.context["rdb"]) as session:
            return orm_enum_to_type[self.type].fetch_from_sql(session, self.id)


def list_nodes(
    info: Info,
    root_type: str,
    root_id: int,
    types: Optional[List[str]] = [
        type
        for type in ProvenanceType
        if type not in ["Concept", "ModelRevision", "Project"]
    ],
    limit: Optional[int] = 1000,
) -> List[Provenance]:

    search_provenance_handler = SearchProvenance(
        rdb=info.context["rdb"], graph_db=info.context["graph_db"]
    )
    search_function = search_provenance_handler["connected_nodes"]
    payload = {
        "root_id": root_id,
        "root_type": root_type,
        "curie": "string",
        "edges": False,
        "nodes": True,
        "types": types,
        "hops": 20,
        "limit": limit,
        "verbose": False,
    }
    results = search_function(payload=payload)

    return [Provenance(**prov) for prov in results.get("nodes")]
