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
from tds.schema.simulation import SimulationRun

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
    if entry_exists(info.context["rdb"].connect(), orm.SimulationRun, run_id):
        with Session(info.context["rdb"]) as session:
            parameters: List[orm.SimulationParameter] = (
                session.query(orm.SimulationParameter)
                .filter(orm.SimulationParameter.run_id == run_id)
                .all()
            )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    to_graphql = lambda param: RunParameter.from_pydantic(
        SimulationParameterSchema.from_orm(param)
    )
    return [to_graphql(param) for param in parameters]


@strawberry.experimental.pydantic.type(model=SimulationRunSchema)
class Run:
    id: strawberry.auto
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


def list_runs(info: Info, simulator_id: Optional[int] = None) -> List[Run]:
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
    to_graphql = lambda run: Run.from_pydantic(SimulationRunSchema.from_orm(run))
    return [to_graphql(run) for run in fetched_runs]


@strawberry.experimental.pydantic.type(model=SimulationPlanSchema)
class Plan:
    id: strawberry.auto
    model_id: strawberry.auto
    simulator: strawberry.auto
    query: strawberry.auto
    content: str

    @strawberry.field
    def runs(self, info: Info) -> List[Run]:
        return list_runs(info, self.id)

    @staticmethod
    def from_pydantic(instance: SimulationPlanSchema) -> "Plan":
        data = instance.dict()
        data["content"] = str(data["content"])
        return Plan(**data)


def list_plans(info: Info) -> List[Plan]:
    fetched_plans: List[orm.SimulationPlan] = list_by_id(
        info.context["rdb"].connect(), orm.SimulationPlan, 100, 0
    )
    to_graphql = lambda plan: Plan.from_pydantic(SimulationPlanSchema.from_orm(plan))
    return [to_graphql(plan) for plan in fetched_plans]
