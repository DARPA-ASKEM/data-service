"""
tds.schema.provenance - API facing provenance schema
"""
from typing import Dict, List, Optional, Type

from pydantic import BaseModel, Field

# pylint: disable=missing-class-docstring
from tds.autogen import schema


class Provenance(schema.Provenance):
    class Config:
        orm_mode = True


class NodeSchema(BaseModel):
    type: str
    id: int
    uuid: str


class ProvenancePayload(BaseModel):
    root_id: Optional[int] = Field(default=1)
    root_type: Optional[schema.ProvenanceType] = Field(default="Publication")
    user_id: Optional[int]
    curie: Optional[str]
    edges: Optional[bool] = Field(default=False)
    nodes: Optional[bool] = Field(default=True)
    types: List[schema.ProvenanceType] = Field(
        default=[
            type
            for type in schema.ProvenanceType
            if type not in ["Concept", "ModelRevision", "Project"]
        ]
    )
    hops: Optional[int] = Field(default=15)
    limit: Optional[int] = Field(default=1000)
    verbose: Optional[bool] = Field(default=False)


provenance_type_to_abbr: Dict[Type[schema.ProvenanceType], str] = {
    schema.ProvenanceType.Dataset: "Ds",
    schema.ProvenanceType.Model: "Md",
    schema.ProvenanceType.ModelConfiguration: "Mc",
    schema.ProvenanceType.Publication: "Pu",
    schema.ProvenanceType.Simulation: "Si",
    schema.ProvenanceType.Project: "Pr",
    schema.ProvenanceType.Concept: "Cn",
}
