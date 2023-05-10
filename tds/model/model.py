from typing import List, Optional

from pydantic import BaseModel

from tds.autogen import orm
from tds.db.base import TdsModel
from tds.model import orm_to_params


class Model(TdsModel):
    name: str
    description: str
    model: dict

    _index = "model"

    # def __init__(self, **kwargs):
    #     for kwarg in kwargs:
    #         setattr(self, kwarg, kwargs[kwarg])

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
        super(Model, self).save(id)

    def _extract_concepts(self):
        pass
