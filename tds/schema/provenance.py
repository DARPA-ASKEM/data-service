"""
tds.schema.provenance - API facing provenance schema
"""
from typing import Dict, Optional, Type

from pydantic import BaseModel

# pylint: disable=missing-class-docstring
from tds.autogen import schema


class Provenance(schema.Provenance):
    class Config:
        orm_mode = True


class ProvenancePayload(BaseModel):
    root_id: Optional[int]
    root_type: Optional[schema.ProvenanceType]
    user_id: Optional[int]
    curie: Optional[str]


provenance_type_to_abbr: Dict[Type[schema.ProvenanceType], str] = {
    schema.ProvenanceType.Dataset: "Ds",
    schema.ProvenanceType.Model: "Md",
    schema.ProvenanceType.Plan: "Sp",
    schema.ProvenanceType.Publication: "Pu",
    schema.ProvenanceType.Intermediate: "In",
    schema.ProvenanceType.SimulationRun: "Sr",
    schema.ProvenanceType.Project: "Pr",
    schema.ProvenanceType.ModelRevision: "Mr",
    schema.ProvenanceType.Concept: "Cn",
    schema.ProvenanceType.ModelParameter: "Mp",
    schema.ProvenanceType.PlanParameter: "Pp",
}
