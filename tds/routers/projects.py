"""
CRUD operations for projects
"""

import json
from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm
from tds.db import entry_exists, list_by_id, request_rdb
from tds.lib.projects import adjust_project_assets, save_project_assets
from tds.operation import create, retrieve, update
from tds.schema.project import Asset, Project, ProjectMetadata
from tds.schema.resource import ResourceType, get_resource_orm

logger = Logger(__name__)
router = APIRouter()


@router.get("")
def list_projects(
    page_size: int = 50, page: int = 0, rdb: Engine = Depends(request_rdb)
) -> List[ProjectMetadata]:
    """
    Retrieve all projects
    """
    return list_by_id(rdb.connect(), orm.Project, page_size, page)


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
def create_project(payload: Project, rdb: Engine = Depends(request_rdb)) -> Response:
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
        content=json.dumps({"id": id}),
    )


@router.post("/{id}", **update.fastapi_endpoint_config)
def update_project(
    id: int, payload: Project, rdb: Engine = Depends(request_rdb)
) -> Response:
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
    return Response(
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )


@router.get(
    "/{project_id}/assets/{resource_type}/{resource_id}",
    **retrieve.fastapi_endpoint_config,
)
def get_asset(id: int, rdb: Engine = Depends(request_rdb)) -> Asset:
    """
    Retrieve asset
    """
    if entry_exists(rdb.connect(), orm.ProjectAsset, id):
        with Session(rdb) as session:
            project_asset = session.query(orm.ProjectAsset).get(id)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Asset.from_orm(project_asset)


@router.post(
    "/{project_id}/assets/{resource_type}/{resource_id}",
    **create.fastapi_endpoint_config,
)
def create_asset(
    project_id: int,
    resource_type: ResourceType,
    resource_id: int,
    rdb: Engine = Depends(request_rdb),
) -> Response:
    """
    Create asset and return its ID
    """
    with Session(rdb) as session:
        identical_count = (
            session.query(orm.ProjectAsset)
            .filter(
                orm.ProjectAsset.project_id == project_id,
                orm.ProjectAsset.resource_id == resource_id,
                orm.ProjectAsset.resource_type == resource_type,
            )
            .count()
        )

        if identical_count == 0:
            project_asset = orm.ProjectAsset(
                project_id=project_id,
                resource_id=resource_id,
                resource_type=resource_type,
            )
            session.add(project_asset)
            session.commit()
            id: int = project_asset.id

            logger.info("new asset created: %i", id)
            return Response(
                status_code=status.HTTP_201_CREATED,
                headers={
                    "content-type": "application/json",
                },
                content=json.dumps({"id": id}),
            )
        return Response(status.HTTP_409_CONFLICT)
