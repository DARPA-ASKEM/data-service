"""
Dataset Schema
"""

from json import dumps
from logging import Logger
from typing import List

import strawberry
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import list_by_id
from tds.experimental.helper import sqlalchemy_type

logger = Logger(__name__)


class DatasetSchema(schema.Dataset):
    @classmethod
    def from_orm(cls, body: orm.SimulationPlan) -> "DatasetSchema":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        setattr(body, "annotations", dumps(body.annotations))
        return super().from_orm(body)

    class Config:
        orm_mode = True


@sqlalchemy_type(orm.Dataset)
@strawberry.experimental.pydantic.type(model=DatasetSchema)
class Dataset:
    id: strawberry.auto
    name: strawberry.auto
    url: strawberry.auto
    description: strawberry.auto
    timestamp: strawberry.auto
    deprecated: strawberry.auto
    sensitivity: strawberry.auto
    quality: strawberry.auto
    temporal_resolution: strawberry.auto
    geospatial_resolution: strawberry.auto
    maintainer: strawberry.auto
    simulation_run: strawberry.auto

    @staticmethod
    def from_pydantic(instance: DatasetSchema) -> "Dataset":
        data = instance.dict()
        del data["annotations"]
        return Dataset(**data)


def list_datasets(info: Info) -> List[Dataset]:
    fetched_datasets: List[orm.Dataset] = list_by_id(
        info.context["rdb"].connect(), orm.Dataset, 100, 0
    )
    return [Dataset.from_orm(dataset) for dataset in fetched_datasets]
