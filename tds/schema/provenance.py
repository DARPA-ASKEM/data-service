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


provenance_type_to_abbr: Dict[
    Type[schema.ProvenanceType], schema.ProvenanceAbbreviations
] = {
    schema.ProvenanceType.Dataset: schema.ProvenanceAbbreviations.Ds,
    schema.ProvenanceType.Model: schema.ProvenanceAbbreviations.Md,
    schema.ProvenanceType.Plan: schema.ProvenanceAbbreviations.Sp,
    schema.ProvenanceType.Publication: schema.ProvenanceAbbreviations.Pu,
    schema.ProvenanceType.Intermediate: schema.ProvenanceAbbreviations.In,
    schema.ProvenanceType.SimulationRun: schema.ProvenanceAbbreviations.Sr,
    schema.ProvenanceType.Project: schema.ProvenanceAbbreviations.Pr,
    schema.ProvenanceType.ModelRevision: schema.ProvenanceAbbreviations.Mr,
    schema.ProvenanceType.Concept: schema.ProvenanceAbbreviations.Cn,
    schema.ProvenanceType.ModelParameter: schema.ProvenanceAbbreviations.Mp,
    schema.ProvenanceType.PlanParameter: schema.ProvenanceAbbreviations.Pp,
}
