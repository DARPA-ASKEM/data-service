"""
tds.schema.provenance - API facing provenance schema
"""
from typing import Dict, Type

# pylint: disable=missing-class-docstring
from tds.autogen import schema


class Provenance(schema.Provenance):
    class Config:
        orm_mode = True


class ProvenancePayload:
    root_id: int
    root_type: schema.ProvenanceType
    search_type: schema.ProvenanceSearchTypes


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
