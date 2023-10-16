"""
TDS Model
"""
from typing import List, Optional

import sqlalchemy as sa
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from tds.db.base import BaseElasticSearchModel, RelationalDatabaseBase
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


class Model(BaseElasticSearchModel):
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
        curies = self._extract_concepts(self.model)
        self.save_concepts(curies)
        if settings.NEO4J_ENABLED:
            self._establish_provenance()
        return res

    def save(self):
        res = super().save()
        curies = self._extract_concepts(self.model)
        self.save_concepts(curies)
        return res

    def save_concepts(self, curies):
        """
        Saves all the curies as concepts associated with the model.
        """
        with Session(pg_engine) as pg_db:
            for curie in curies:
                # @TODO: Break this code out for reuse where other
                # data types can use it to handle concepts.

                if (
                    pg_db.query(ActiveConcept)
                    .filter(ActiveConcept.curie == curie)
                    .count()
                    == 0
                ):
                    mark_concept_active(pg_db, curie)
                concept = (
                    pg_db.query(ActiveConcept)
                    .filter(ActiveConcept.curie == curie)
                    .first()
                )

                if concept.name not in self.concepts:
                    concept_association = OntologyConcept(
                        curie=curie,
                        type="models",
                        object_id=self.id,
                        status="obj",
                    )
                    pg_db.add(concept_association)
                    self.concepts.append(concept.name)
            pg_db.commit()

    @classmethod
    def _extract_concepts(cls, head):
        """
        Method extracts concepts from the model and saves them to the db.
        """
        concepts = set()
        if isinstance(head, dict):
            if "grounding" in head:
                for key, value in head["grounding"].get("identifiers", {}).items():
                    curie = f"{key}:{value}"
                    concepts.add(curie)
            children = head.values()
        elif isinstance(head, list):
            children = head
        else:
            return concepts
        for child in children:
            concepts.update(cls._extract_concepts(child))
        return concepts

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


class ModelFramework(RelationalDatabaseBase):
    """
    ModelFramework Data Model.
    """

    __tablename__ = "model_framework"

    name = sa.Column(sa.String(), primary_key=True)
    version = sa.Column(sa.String(), nullable=False)
    semantics = sa.Column(sa.String(), nullable=False)
    schema_url = sa.Column(sa.String(), nullable=False)


class ModelFrameworkPayload(BaseModel):
    """
    ModelFrameworkPayload Model.
    """

    name: str
    version: str
    semantics: str
    schema_url: Optional[str]
