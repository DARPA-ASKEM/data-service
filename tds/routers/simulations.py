"""
CRUD operations for plans and runs
"""
import json
from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
from tds.db import entry_exists, request_rdb
from tds.operation import create, delete, retrieve
from tds.schema.simulation import Plan, Run

logger = Logger(__name__)
router = APIRouter()


@router.get("/plans")
def list_plans(rdb: Engine = Depends(request_rdb)) -> List[Plan]:
    """
    Retrieve all plans
    """
    print("her")
    run = []
    with Session(rdb) as session:
        for entry in session.query(orm.SimulationPlan).all():
            parameters: Query[orm.SimulationParameter] = session.query(
                orm.SimulationParameter
            ).filter(orm.SimulationParameter.id == entry.id)
            print(entry)
            print("he")
            print(parameters)
            print(list(parameters))
            run.append(Plan.from_orm(entry, list(parameters)))
    return run


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
            ).filter(orm.SimulationParameter.id == id)
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
        # parameters = plan_payload.pop("parameters")
        plan_payload.pop("id")
        plan = orm.SimulationPlan(**plan_payload)
        session.add(plan)
        session.commit()
        id: int = plan.id
        # for name, (value, type) in parameters.items():
        #     session.add(
        #         orm.SimulationParameter(plan_id=id, name=name, value=value, type=type)
        #     )
        session.commit()
    logger.info("new plan created: %i", id)
    return Response(
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )


@router.get("/run", **retrieve.fastapi_endpoint_config)
def list_runs(rdb: Engine = Depends(request_rdb)) -> List[Plan]:
    """
    Retrieve all simulation run for all plans
    """
    with Session(rdb) as session:
        return list(session.query(orm.SimulationRun).all())


@router.get("/run/description/{id}", **retrieve.fastapi_endpoint_config)
def get_run_descriptoin(id: int, rdb: Engine = Depends(request_rdb)) -> Run:
    """
    Retrieve results metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.SimulationRun).filter(orm.SimulationRun.id == id).count()
            == 1
        ):
            return Run.from_orm(session.query(orm.SimulationRun).get(id))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/run/verbose", **create.fastapi_endpoint_config)
def create_verbose_run(payload: Run, rdb: Engine = Depends(request_rdb)) -> int:
    """
    Create results metadata
    """
    with Session(rdb) as session:
        run_payload = payload.dict()
        run = orm.SimulationRun(**run_payload)
        session.add(run)
        session.commit()
        id: int = run.id

    logger.info("new results with %i", id)
    return Response(
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )


@router.delete("/run/verbose/{id}", **delete.fastapi_endpoint_config)
def delete_verbose_run(id: int, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Delete run metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.SimulationRun).filter(orm.SimulationRun.id == id).count()
            == 1
        ):
            run = session.query(orm.SimulationRun).get(id)
            session.delete(run)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.get("/run/{id}", **retrieve.fastapi_endpoint_config)
def get_run(id: int, rdb: Engine = Depends(request_rdb)) -> Run:
    """
    Retrieve run metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.SimulationRun).filter(orm.SimulationRun.id == id).count()
            == 1
        ):
            return Run.from_orm(session.query(orm.SimulationRun).get(id))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/run", **create.fastapi_endpoint_config)
def create_run(payload: Run, rdb: Engine = Depends(request_rdb)) -> int:
    """
    Create run metadata
    """
    with Session(rdb) as session:
        run_payload = payload.dict()
        run = orm.SimulationRun(**run_payload)
        session.add(run)
        session.commit()
        id: int = run.id
    logger.info("new run with %i", id)
    return Response(
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )


@router.delete("/run/{id}", **delete.fastapi_endpoint_config)
def delete_run(id: int, rdb: Engine = Depends(request_rdb)) -> Response:
    """
    Delete run metadata
    """
    with Session(rdb) as session:
        if (
            session.query(orm.SimulationRun).filter(orm.SimulationRun.id == id).count()
            == 1
        ):
            run = session.query(orm.SimulationRun).get(id)
            session.delete(run)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
