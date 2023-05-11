from typing import List, Optional

from pydantic import Field
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
from tds.db.base import TdsModel
from tds.db.relational import engine as pg_engine
from tds.lib.concepts import mark_concept_active
from tds.modules.model.utils import orm_to_params


class Model(TdsModel):
    name: str
    description: str
    model: dict
    model_schema: str = Field(alias="schema")
    model_version: str

    _index = "model"
    concepts: Optional[List] = []

    @classmethod
    def from_orm(
        cls,
        parameters: List,
    ) -> "Model":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        body.__dict__["content"] = dumps(ModelContent.from_orm(state).content)
        body.__dict__["parameters"] = orm_to_params(parameters)
        return super().from_orm(body)

    def save(self, id: Optional[None | str | int] = None):
        res = super(Model, self).save(id)
        # Pass the model id so we have it for association.
        self._extract_concepts(res["_id"])
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
