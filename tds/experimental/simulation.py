"""
Simulation Schema
"""

from json import dumps
from logging import Logger
from typing import List, Optional

import strawberry
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from strawberry.types import Info

from tds.autogen import orm, schema
from tds.db import entry_exists, list_by_id
from tds.experimental.enum import ValueType
from tds.experimental.helper import sqlalchemy_type
from tds.experimental.model import Model

logger = Logger(__name__)


class SimulationParameterSchema(schema.SimulationParameter):
    class Config:
        orm_mode = True


class SimulationRunSchema(schema.SimulationRun):
    class Config:
        orm_mode = True


class SimulationPlanSchema(schema.SimulationPlan):
    @classmethod
    def from_orm(cls, body: orm.SimulationPlan) -> "SimulationPlanSchema":
        """
        Handle ORM conversion while coercing `dict` to JSON
        """
        setattr(body, "content", dumps(body.content))
        return super().from_orm(body)

    class Config:
        orm_mode = True


@sqlalchemy_type(orm.SimulationParameter)
@strawberry.experimental.pydantic.type(model=SimulationParameterSchema)
class RunParameter:
    id: strawberry.auto
    run_id: strawberry.auto
    name: strawberry.auto
    value: strawberry.auto
    type: ValueType

    @staticmethod
    def from_pydantic(instance: SimulationParameterSchema) -> "RunParameter":
        data = instance.dict()
        data["type"] = ValueType(data["type"].name)
        return RunParameter(**data)


def list_parameters(run_id: int, info: Info) -> List[RunParameter]:
    with Session(info.context["rdb"]) as session:
        parameters: List[orm.SimulationParameter] = (
            session.query(orm.SimulationParameter)
            .filter(orm.SimulationParameter.run_id == run_id)
            .all()
        )
    return [RunParameter.from_orm(param) for param in parameters]


@sqlalchemy_type(orm.SimulationRun)
@strawberry.experimental.pydantic.type(model=SimulationRunSchema)
class Run:
    id: strawberry.auto
    description: strawberry.auto
    simulator_id: strawberry.auto
    timestamp: strawberry.auto
    completed_at: strawberry.auto
    success: strawberry.auto
    dataset_id: strawberry.auto
    response: str

    @strawberry.field
    def parameters(self, info: Info) -> List[RunParameter]:
        return list_parameters(self.id, info)

    @staticmethod
    def from_pydantic(instance: SimulationRunSchema) -> "Run":
        data = instance.dict()
        data["response"] = str(data["response"])
        return Run(**data)


def list_runs(
    info: Info, simulator_id: Optional[int] = None, ids: Optional[List[int]] = None
) -> List[Run]:
    if ids is not None and simulator_id is not None:
        raise Exception("Conflicting search terms given")

    if ids is not None:
        with Session(info.context["rdb"]) as session:
            return Run.fetch_from_sql(session, ids)

    if simulator_id is not None:
        with Session(info.context["rdb"]) as session:
            fetched_runs: List[orm.SimulationRun] = (
                session.query(orm.SimulationRun)
                .filter(orm.SimulationRun.simulator_id == simulator_id)
                .all()
            )
    else:
        fetched_runs: List[orm.SimulationRun] = list_by_id(
            info.context["rdb"].connect(), orm.SimulationRun, 100, 0
        )
    return [Run.from_orm(run) for run in fetched_runs]


@sqlalchemy_type(orm.SimulationPlan)
@strawberry.experimental.pydantic.type(model=SimulationPlanSchema)
class Plan:
    id: strawberry.auto
    model_id: strawberry.auto
    simulator: strawberry.auto
    query: strawberry.auto
    content: str

    @strawberry.field
    def model(self, info: Info) -> Model:
        if entry_exists(info.context["rdb"].connect(), orm.Model, self.model_id):
            with Session(info.context["rdb"]) as session:
                model = session.query(orm.Model).get(self.model_id)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return Model.from_orm(model)

    @strawberry.field
    def runs(self, info: Info) -> List[Run]:
        return list_runs(info, self.id)

    @staticmethod
    def from_pydantic(instance: SimulationPlanSchema) -> "Plan":
        data = instance.dict()
        data["content"] = str(data["content"])
        return Plan(**data)


def list_plans(info: Info, ids: Optional[List[int]] = None) -> List[Plan]:
    if ids is not None:
        with Session(info.context["rdb"]) as session:
            return Plan.fetch_from_sql(session, ids)

    fetched_plans: List[orm.SimulationPlan] = list_by_id(
        info.context["rdb"].connect(), orm.SimulationPlan, 100, 0
    )
    return [Plan.from_orm(plan) for plan in fetched_plans]
