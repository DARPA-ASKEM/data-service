from typing import List, Optional

from pydantic import Field
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
from tds.db import ProvenanceHandler, request_graph_db
from tds.db.base import TdsModel
from tds.db.relational import engine as pg_engine
from tds.lib.concepts import mark_concept_active
from tds.schema.provenance import Provenance
from tds.settings import settings


class Model(TdsModel):
    name: str
    description: str
    model: dict
    model_schema: str = Field(alias="schema")
    model_version: str

    _index = "model"
    concepts: Optional[List] = []

    def save(self, model_id: Optional[None | str | int] = None):
        res = super(Model, self).save(model_id)
        # Pass the model id so we have it for association.
        self._extract_concepts(res["_id"])
        if settings.NEO4J_ENABLED:
            self._establish_provenance()
        return res

    def _extract_concepts(self, model_id):
        """
        Method extracts concepts from the model and saves them to the db.
        """
        states = self.model["states"]
        curies = []
        with Session(pg_engine) as pg_db:
            for state in states:
                if (
                    "grounding" in state
                    and "identifiers" in state["grounding"]
                    and bool(state["grounding"]["identifiers"])
                ):
                    for key in state["grounding"]["identifiers"]:
                        value = state["grounding"]["identifiers"][key]
                        curie = f"{key}:{value}"
                        # @TODO: Break this code out for reuse where other data types can use it to handle concepts.
                        concept = (
                            pg_db.query(orm.ActiveConcept)
                            .filter(orm.ActiveConcept.curie == curie)
                            .first()
                        )
                        if concept is None:
                            mark_concept_active(pg_db, curie)
                            concept = (
                                pg_db.query(orm.ActiveConcept)
                                .filter(orm.ActiveConcept.curie == curie)
                                .first()
                            )

                        if concept.name not in self.concepts:
                            curies.append(
                                curie
                            )  # Append to local list to prevent repeated queries.
                            concept_association = orm.OntologyConcept(
                                curie=curie,
                                type="models",
                                object_id=model_id,
                                status="obj",
                            )
                            pg_db.add(concept_association)
                            pg_db.commit()
                            self.concepts.append(concept.name)

    def _establish_provenance(self):
        # add ModelParameter nodes
        provenance_handler = ProvenanceHandler(
            rdb=pg_engine, graph_db=request_graph_db()
        )

        with Session(pg_engine) as session:
            model = session.query(orm.ModelDescription).get(id)
            payload = Provenance(
                left=self.id,
                left_type="Model",
                right=model.state_id,
                right_type="ModelRevision",
                relation_type="BEGINS_AT",
                user_id=None,
                concept=".",
            )

            provenance_handler.create_entry(payload)
