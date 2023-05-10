from typing import List, Optional

from pydantic import BaseModel, Field

from tds.autogen import orm
from tds.db.base import TdsModel
from tds.modules.model.utils import orm_to_params


class Model(TdsModel):
    name: str
    description: str
    model: dict
    model_schema: str = Field(alias="schema")
    model_version: float

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
        self._extract_concepts()
        return super(Model, self).save(id)

    def _extract_concepts(self):
        states = self.model["states"]

        for state in states:
            if (
                "grounding" in state
                and "identifiers" in state["grounding"]
                and bool(state["grounding"]["identifiers"])
            ):
                for key in state["grounding"]["identifiers"]:
                    value = state["grounding"]["identifiers"][key]
                    curie = f"{key}:{value}"
                    if curie not in self.concepts:
                        self.concepts.append(curie)
