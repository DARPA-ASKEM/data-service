"""
CRUD operations for projects
"""

import json
from collections import defaultdict
from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session

from tds.autogen import orm, schema
from tds.db import entry_exists, list_by_id, request_rdb
from tds.lib.projects import adjust_project_assets, save_project_assets
from tds.operation import create, delete, retrieve, update
from tds.schema.model import Intermediate, Model, ModelDescription
from tds.schema.project import Project, ProjectMetadata
from tds.schema.resource import (
    Publication,
    ResourceType,
    Software,
    get_resource_orm,
    map_resource_str_orm,
)
from tds.schema.simulation import (
    Plan,
    Run,
    RunDescription,
    SimulationParameters,
    orm_to_params,
)

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


def return_asset(asset, session):

    orm = get_resource_orm(asset.resource_type)
    print(orm)
    print(asset.resource_type)
    if asset.resource_type == "publications":
        return Publication.from_orm(session.query(orm).get(asset.resource_id))
    elif asset.resource_type == "models":
        print("here")
        print(asset)
        return ModelDescription.from_orm(session.query(orm).get(asset.resource_id))
    elif asset.resource_type == "intermediates":
        return Intermediate.from_orm(session.query(orm).get(asset.resource_id))
    elif asset.resource_type == "plans":
        return Plan.from_orm(session.query(orm).get(asset.resource_id))
    elif asset.resource_type == "simulation_runs":
        return RunDescription.from_orm(session.query(orm).get(asset.resource_id))
    else:
        return session.query(orm).get(asset.resource_id)


@router.get("/{id}", **retrieve.fastapi_endpoint_config)
def get_project(id: int, rdb: Engine = Depends(request_rdb)) -> Project:
    """
    Retrieve project
    """
    if entry_exists(rdb.connect(), orm.Project, id):
        with Session(rdb) as session:
            project = session.query(orm.Project).get(id)
            assets: Query[orm.ProjectAsset] = session.query(orm.ProjectAsset).filter(
                orm.ProjectAsset.project_id == id
            )
            assets_ = defaultdict(list)
            for asset in list(assets):

                assets_[asset.resource_type].append(
                    return_asset(asset, session=session)
                )
            print("here")
            print(assets_.keys())
            # print(assets_['intermediates'])
            print(type(assets_))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Project.from_orm(project, assets_)


@router.delete("/{id}", **retrieve.fastapi_endpoint_config)
def deactivate_project(id: int, rdb: Engine = Depends(request_rdb)) -> Project:
    """
    Deactivate project
    """
    if entry_exists(rdb.connect(), orm.Project, id):
        with Session(rdb) as session:
            project = session.query(orm.Project).get(id)

        # set to dict and active to false
        project_ = project.__dict__
        project_.pop("_sa_instance_state")
        project_["active"] = False

        with Session(rdb) as session:
            session.query(orm.Project).filter(orm.Project.id == id).update(project_)
            session.commit()

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id, "status": project_["active"]}),
    )


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


@router.put("/{id}", **update.fastapi_endpoint_config)
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


@router.delete(
    "/{project_id}/assets/{resource_type}/{resource_id}",
    **delete.fastapi_endpoint_config,
)
def delete_asset(
    project_id: int,
    resource_type: ResourceType,
    resource_id: int,
    rdb: Engine = Depends(request_rdb),
) -> Response:
    """
    Remove asset
    """
    with Session(rdb) as session:
        project_assets = list(
            session.query(orm.ProjectAsset).filter(
                orm.ProjectAsset.project_id == project_id,
                orm.ProjectAsset.resource_type == resource_type,
                orm.ProjectAsset.resource_id == resource_id,
            )
        )
        if len(project_assets) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        session.delete(project_assets[0])
        session.commit()
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
        )


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
