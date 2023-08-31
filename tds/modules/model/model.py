"""
TDS Model
"""
from typing import List, Optional

import sqlalchemy as sa
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from tds.db.base import Base, TdsModel
from tds.db.relational import engine as pg_engine
from tds.lib.concepts import mark_concept_active
from tds.lib.model_configs import model_config
from tds.modules.concept.model import ActiveConcept, OntologyConcept
from tds.settings import settings


class Header(BaseModel):
    """
    Header object for AMR
    """

    name: str
    description: str
    model_schema: Optional[str] = Field(alias="schema")
    schema_name: Optional[str]
    model_version: str


class Model(TdsModel):
    """
    TDS Model Data Model
    """

    header: Header
    username: Optional[str]
    model: dict
    semantics: Optional[dict]
    metadata: Optional[dict]

    _index = "model"
    concepts: Optional[List] = []
    _exists = False

    def create(self):
        res = super().create()
        self._extract_concepts()
        if settings.NEO4J_ENABLED:
            self._establish_provenance()
        return res

    def save(self):
        res = super().save()
        self._extract_concepts()
        return res

    def _extract_concepts(self):
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
                        # @TODO: Break this code out for reuse where other
                        # data types can use it to handle concepts.
                        concept = (
                            pg_db.query(ActiveConcept)
                            .filter(ActiveConcept.curie == curie)
                            .first()
                        )
                        if concept is None:
                            mark_concept_active(pg_db, curie)
                            concept = (
                                pg_db.query(ActiveConcept)
                                .filter(ActiveConcept.curie == curie)
                                .first()
                            )

                        if concept.name not in self.concepts:
                            curies.append(
                                curie
                            )  # Append to local list to prevent repeated queries.
                            concept_association = OntologyConcept(
                                curie=curie,
                                type="models",
                                object_id=self.id,
                                status="obj",
                            )
                            pg_db.add(concept_association)
                            pg_db.commit()
                            self.concepts.append(concept.name)

    def _establish_provenance(self):
        # add ModelParameter nodes
        # provenance_handler = ProvenanceHandler(rdb=pg_engine, graph_db=ENGINE)
        #
        # payload = Provenance(
        #     left=self.id,
        #     left_type="Model",
        #     right=self.id,
        #     right_type="ModelRevision",
        #     relation_type="BEGINS_AT" if self._exists is False else "EDITED_FROM",
        #     user_id=None,
        #     concept=".",
        # )
        #
        # provenance_handler.create_entry(payload)
        pass

    class Config:
        """
        TDS Model Swagger Example.
        """

        schema_extra = {"example": model_config}


class ModelFramework(Base):
    """
    ModelFramework Data Model.
    """

    __tablename__ = "model_framework"

    name = sa.Column(sa.String(), primary_key=True)
    version = sa.Column(sa.String(), nullable=False)
    semantics = sa.Column(sa.String(), nullable=False)
    schema_url = sa.Column(sa.String())


class ModelFrameworkPayload(BaseModel):
    """
    ModelFrameworkPayload Model.
    """

    name: str
    version: str
    semantics: str
    schema_url: Optional[str]
