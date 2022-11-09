"""
tds.router.projects - crud operations for projects
"""

from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
from tds.autogen.schema import RelationType
from tds.db import (
    ProvenanceHandler,
    entry_exists,
    request_provenance_handler,
    request_rdb,
)
from tds.operation import create, retrieve, update
from tds.schema.project import Project
from tds.schema.resources import get_resource_orm

logger = Logger(__name__)
router = APIRouter()


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
                [
                    entry_exists(rdb.connect(), current_orm, id)
                    for id in assets[resource_type]
                ]
            ):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Not all listed assets exist.",
                )
        project = orm.Project(**project_payload)
        session.add(project)
        session.commit()
        id: int = project.id
        for resource_type, resource_ids in assets.items():
            assets = [
                orm.ProjectAsset(
                    project_id=id,
                    resource_id=resource_id,
                    resource_type=resource_type,
                    external_ref="",
                )
                for resource_id in resource_ids
            ]
            session.bulk_save_objects(assets)
        session.commit()
    logger.info("new project created: %i", id)
    return id
