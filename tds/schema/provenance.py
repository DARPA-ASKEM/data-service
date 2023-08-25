"""
tds.schema.provenance - API facing provenance schema
"""
from typing import Dict, List, Optional, Type

from pydantic import BaseModel, Field

# pylint: disable=missing-class-docstring
from tds.db.enums import ProvenanceType
from tds.modules.provenance.model import Provenance as ProvenanceModel


class Provenance(ProvenanceModel):
    class Config:
        orm_mode = True


class NodeSchema(BaseModel):
    type: str
    id: int
    uuid: str


class ProvenancePayload(BaseModel):
    root_id: Optional[str] = Field(default=1)
    root_type: Optional[ProvenanceType] = Field(default="Publication")
    user_id: Optional[int]
    curie: Optional[str]
    edges: Optional[bool] = Field(default=False)
    nodes: Optional[bool] = Field(default=True)
    types: List[ProvenanceType] = Field(
        default=[
            type
            for type in ProvenanceType
            if type not in ["Concept", "ModelRevision", "Project"]
        ]
    )
    hops: Optional[int] = Field(default=15)
    limit: Optional[int] = Field(default=1000)
    verbose: Optional[bool] = Field(default=False)


provenance_type_to_abbr: Dict[Type[ProvenanceType], str] = {
    ProvenanceType.Dataset: "Ds",
    ProvenanceType.Model: "Md",
    ProvenanceType.ModelConfiguration: "Mc",
    ProvenanceType.Publication: "Pu",
    ProvenanceType.Simulation: "Si",
    ProvenanceType.Project: "Pr",
    ProvenanceType.Concept: "Cn",
    ProvenanceType.Artifact: "Ar",
    ProvenanceType.Code: "Co",
}
