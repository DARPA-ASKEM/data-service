"""
tds.router.projects - crud operations for projects
"""

import json
from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
from tds.db import entry_exists, request_rdb
from tds.lib.projects import adjust_project_assets, save_project_assets
from tds.operation import create, retrieve, update
from tds.schema.project import Project
from tds.schema.resources import get_resource_orm

logger = Logger(__name__)
router = APIRouter()


@router.get("")
def list_projects(rdb: Engine = Depends(request_rdb)) -> List[Project]:
    """
    Retrieve all projects
    """
    results = []
    with Session(rdb) as session:
        for entry in session.query(orm.Project).all():
            assets: Query[orm.ProjectAsset] = session.query(orm.ProjectAsset).filter(
                orm.ProjectAsset.resource_id == entry.id
            )
            results.append(Project.from_orm(entry, list(assets)))
    return results


@router.get("/{id}", **retrieve.fastapi_endpoint_config)
def get_project(id: int, rdb: Engine = Depends(request_rdb)) -> Project:
    """
    Retrieve project
    """
    if entry_exists(rdb.connect(), orm.Project, id):
        with Session(rdb) as session:
            project = session.query(orm.Project).get(id)
            parameters: Query[orm.ProjectAsset] = session.query(
                orm.ProjectAsset
            ).filter(orm.ProjectAsset.project_id == id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Project.from_orm(project, list(parameters))


@router.post("", **create.fastapi_endpoint_config)
def create_project(payload: Project, rdb: Engine = Depends(request_rdb)) -> int:
    """
    Create project and return its ID
    """
    with Session(rdb) as session:
        project_payload = payload.dict()
        # pylint: disable-next=unused-variable
        concept_payload = project_payload.pop("concept")  # TODO: Save ontology term
        assets = project_payload.pop("assets")
        for resource_type in assets:
            current_orm = get_resource_orm(resource_type)
            if not all(
                (
                    entry_exists(rdb.connect(), current_orm, id)
                    for id in assets[resource_type]
                )
            ):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Not all listed assets exist.",
                )
        project = orm.Project(**project_payload)
        session.add(project)
        session.commit()
        id: int = project.id
        save_project_assets(id, assets, session)
        session.commit()
    logger.info("new project created: %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "location": f"/api/projects/{id}",
            "content-type": "application/json",
        },
        content=json.dumps({"project_id": id}),
    )


@router.post("/{id}", **update.fastapi_endpoint_config)
def update_project(
    id: int, payload: Project, rdb: Engine = Depends(request_rdb)
) -> int:
    """
    Update project
    """
    if entry_exists(rdb.connect(), orm.Project, id):
        project_payload = payload.dict()
        project_payload.pop("concept")  # TODO: Save ontology term
        project_payload.pop("id")
        assets = project_payload.pop("assets")
        with Session(rdb) as session:
            session.query(orm.Project).filter(orm.Project.id == id).update(
                project_payload
            )
            adjust_project_assets(id, assets, session)
            session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return id
