"""
tds.router.simulations - crud operations for plans and runs
"""

from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
from tds.db import entry_exists, request_rdb
from tds.operation import create, delete, retrieve
from tds.schema.simulation import Plan, Results

logger = Logger(__name__)
router = APIRouter()


@router.get("/plans")
def list_plans(rdb: Engine = Depends(request_rdb)) -> List[Plan]:
    """
    Retrieve all plans
    """
    results = []
    with Session(rdb) as session:
        for entry in session.query(orm.SimulationPlan).all():
            parameters: Query[orm.SimulationParameter] = session.query(
                orm.SimulationParameter
            ).filter(orm.SimulationParameter.plan_id == entry.id)
            results.append(Plan.from_orm(entry, list(parameters)))
    return results


@router.get("/plans/{id}", **retrieve.fastapi_endpoint_config)
def get_plan(id: int, rdb: Engine = Depends(request_rdb)) -> Plan:
    """
    Retrieve plan
    """
    if entry_exists(rdb.connect(), orm.SimulationPlan, id):
        with Session(rdb) as session:
            plan = session.query(orm.SimulationPlan).get(id)
            parameters: Query[orm.SimulationParameter] = session.query(
                orm.SimulationParameter
            ).filter(orm.SimulationParameter.plan_id == id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Plan.from_orm(plan, list(parameters))


@router.post("/plans", **create.fastapi_endpoint_config)
def create_plan(payload: Plan, rdb: Engine = Depends(request_rdb)) -> int:
    """
    Create plan and return its ID
    """
    with Session(rdb) as session:
        plan_payload = payload.dict()
        # pylint: disable-next=unused-variable
        concept_payload = plan_payload.pop("concept")  # TODO: Save ontology term
        parameters = plan_payload.pop("parameters")
        plan_payload.pop("id")
        plan = orm.SimulationPlan(**plan_payload)
        session.add(plan)
        session.commit()
        id: int = plan.id
        for name, (value, type) in parameters.items():
            session.add(
                orm.SimulationParameter(plan_id=id, name=name, value=value, type=type)
            )
        session.commit()
    logger.info("new plan created: %i", id)
    return id


@router.get("/results", **retrieve.fastapi_endpoint_config)
def list_results(rdb: Engine = Depends(request_rdb)) -> List[Plan]:
    """
    Retrieve all simulation results for all plans
    """
    with Session(rdb) as session:
        return list(session.query(orm.SimulationRun).all())


@router.get("/results/{id}", **retrieve.fastapi_endpoint_config)
def get_results(id: int, rdb: Engine = Depends(request_rdb)) -> Results:
    """
    Retrieve software metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.SimulationRun).filter(orm.SimulationRun.id == id).count()
            == 1
        ):
            return Results.from_orm(session.query(orm.SimulationRun).get(id))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/results", **create.fastapi_endpoint_config)
def create_results(payload: Results, rdb: Engine = Depends(request_rdb)) -> int:
    """
    Create software metadata
    """
    with Session(rdb) as session:
        results_payload = payload.dict()
        results = orm.SimulationRun(**results_payload)
        session.add(results)
        session.commit()
        id: int = results.id
    logger.info("new software with %i", id)
    return id


@router.delete("/results/{id}", **delete.fastapi_endpoint_config)
def delete_results(id: int, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Delete software metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.SimulationRun).filter(orm.SimulationRun.id == id).count()
            == 1
        ):
            results = session.query(orm.SimulationRun).get(id)
            session.delete(results)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
