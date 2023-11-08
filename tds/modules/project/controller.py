"""
CRUD operations for Project
"""
from logging import Logger
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query as FastAPIQuery
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query, Session
from sqlalchemy.orm.exc import NoResultFound

from tds.db import entry_exists, es_client, request_rdb
from tds.db.enums import ResourceType
from tds.modules.project.helpers import (
    ResourceDoesNotExist,
    adjust_project_assets,
    es_list_response,
    es_resources,
    save_project,
)
from tds.modules.project.model import Project, ProjectAsset, ProjectPayload
from tds.modules.project.response import ProjectResponse
from tds.operation import create, delete, retrieve, update
from tds.schema.resource import get_resource_orm
from tds.settings import settings

project_router = APIRouter()
logger = Logger(__name__)
es = es_client()


@project_router.get(
    "", response_model=list[ProjectResponse], **retrieve.fastapi_endpoint_config
)
def list_projects(
    include_inactive: bool = False, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Retrieve the list of projects.
    """
    with Session(rdb) as session:
        if include_inactive is True:
            projects = session.query(Project).all()
        else:
            projects = session.query(Project).filter(Project.active).all()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={"content-type": "application/json"},
        content=jsonable_encoder(projects),
    )


@project_router.post("", **create.fastapi_endpoint_config)
def project_post(
    payload: ProjectPayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Create project and return its ID
    """
    try:
        with Session(rdb) as session:
            project_payload = payload.dict()
            if "concept" in project_payload:
                # pylint: disable-next=unused-variable
                concept_payload = project_payload.pop(
                    "concept"
                )  # TODO: Save ontology term

            project = save_project(project=project_payload, session=session)

            project_id: int = project.id

        logger.info("new project created: %i", project_id)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            headers={
                "location": f"/api/projects/{project_id}",
                "content-type": "application/json",
            },
            content={"id": project_id},
        )
    except ResourceDoesNotExist as error:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers={"content-type": "application/json"},
            content={"message": error.message},
        )


@project_router.get(
    "/{project_id}", response_model=ProjectResponse, **retrieve.fastapi_endpoint_config
)
def project_get(project_id: int, rdb: Engine = Depends(request_rdb)) -> JSONResponse:
    """
    Retrieve a project from ElasticSearch
    """
    try:
        if entry_exists(rdb.connect(), Project, project_id):
            with Session(rdb) as session:
                project = session.query(Project).get(project_id)
                # pylint: disable-next=unused-variable
                parameters: Query[ProjectAsset] = session.query(ProjectAsset).filter(
                    ProjectAsset.project_id == project_id
                )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={"content-type": "application/json"},
            content=jsonable_encoder(project),
        )
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={"content-type": "application/json"},
            content={"message": f"The project with id {project_id} was not found."},
        )


@project_router.put("/{project_id}", **update.fastapi_endpoint_config)
def project_put(
    project_id: int, payload: ProjectPayload, rdb: Engine = Depends(request_rdb)
) -> JSONResponse:
    """
    Update a project.
    """
    try:
        if entry_exists(rdb.connect(), Project, project_id):
            with Session(rdb) as session:
                project_payload = payload.dict()
                assets = project_payload.pop("assets")
                if "concept" in project_payload:
                    # pylint: disable-next=unused-variable
                    concept_payload = project_payload.pop(
                        "concept"
                    )  # TODO: Save ontology term

                session.query(Project).filter(Project.id == project_id).update(
                    project_payload
                )
                adjust_project_assets(project_id, assets, session)
                session.commit()

            logger.info("new project created: %i", project_id)
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                headers={"content-type": "application/json"},
                content={"id": project_id},
            )

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except ResourceDoesNotExist as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={"content-type": "application/json"},
            content={"message": error.message},
        )


@project_router.delete("/{project_id}", **delete.fastapi_endpoint_config)
def project_delete(project_id: int, rdb: Engine = Depends(request_rdb)) -> JSONResponse:
    """
    Deactivate project
    """
    try:
        if entry_exists(rdb.connect(), Project, project_id):
            with Session(rdb) as session:
                project = session.query(Project).get(project_id)

            # set to dict and active to false
            project_ = project.__dict__
            project_.pop("_sa_instance_state")
            project_["active"] = False

            with Session(rdb) as session:
                session.query(Project).filter(Project.id == project_id).update(project_)
                session.commit()

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(
            headers={"content-type": "application/json"},
            content={"id": project_id, "status": project_["active"]},
        )
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={"content-type": "application/json"},
            content={
                "id": project_id,
                "message": f"Project with ID {project_id} not found.",
            },
        )


@project_router.delete(
    "/{project_id}/assets/{resource_type}/{resource_id}",
    **delete.fastapi_endpoint_config,
)
def delete_asset(
    project_id: int,
    resource_type: ResourceType,
    resource_id: int | str,
    rdb: Engine = Depends(request_rdb),
) -> JSONResponse:
    """
    Remove asset
    """
    with Session(rdb) as session:
        project_assets = list(
            session.query(ProjectAsset).filter(
                ProjectAsset.project_id == project_id,
                ProjectAsset.resource_type == resource_type,
                ProjectAsset.resource_id == str(resource_id),
            )
        )
        if len(project_assets) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        # Loop through assets because the result is an array and if there are
        # more than one result, we want to remove it anyway.
        for asset in project_assets:
            session.delete(asset)
        session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={"content-type": "application/json"},
            content={"message": "Asset has been deleted."},
        )


@project_router.post(
    "/{project_id}/assets/{resource_type}/{resource_id}",
    **create.fastapi_endpoint_config,
)
def create_asset(
    project_id: int,
    resource_type: ResourceType,
    resource_id: int | str,
    rdb: Engine = Depends(request_rdb),
) -> JSONResponse:
    """
    Create asset and return its ID
    """
    with Session(rdb) as session:
        identical_count = (
            session.query(ProjectAsset)
            .filter(
                ProjectAsset.project_id == project_id,
                ProjectAsset.resource_id == str(resource_id),
                ProjectAsset.resource_type == resource_type,
            )
            .count()
        )

        if identical_count == 0:
            project_asset = ProjectAsset(
                project_id=project_id,
                resource_id=str(resource_id),
                resource_type=resource_type,
            )
            session.add(project_asset)
            session.commit()
            asset_id: int = project_asset.id

            logger.info("new asset created: %i", asset_id)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                headers={"content-type": "application/json"},
                content={"id": asset_id},
            )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            headers={"content-type": "application/json"},
            content={"message": "Asset already exists for project."},
        )


@project_router.get("/{project_id}/assets", **retrieve.fastapi_endpoint_config)
def get_project_assets(
    project_id: int,
    types: Optional[List[ResourceType]] = FastAPIQuery(
        default=[
            ResourceType.datasets,
            ResourceType.models,
            ResourceType.model_configurations,
            ResourceType.publications,
            ResourceType.simulations,
            ResourceType.workflows,
            ResourceType.artifacts,
            ResourceType.code,
            ResourceType.documents,
            ResourceType.equations,
        ]
    ),
    rdb: Engine = Depends(request_rdb),
) -> JSONResponse:
    """
    Retrieve project assets
    """
    if entry_exists(rdb.connect(), Project, project_id):
        with Session(rdb) as session:
            project = session.query(Project).get(project_id)
            assets = project.assets
            assets_key_ids = {type: [] for type in types}
            for asset in list(assets):
                if asset.resource_type in types:
                    assets_key_ids[asset.resource_type].append(asset.resource_id)

            assets_key_objects = {}
            for key in assets_key_ids:
                orm_type = get_resource_orm(key)
                if key in es_resources:
                    responder = es_list_response[key]
                    index_singular = key if key[-1] != "s" else key.rstrip("s")
                    index = f"{settings.ES_INDEX_PREFIX}{index_singular}"
                    es_items = es.search(
                        index=index,
                        query={"ids": {"values": assets_key_ids[key]}},
                        fields=responder["fields"],
                        size=1000,
                    )
                    assets_key_objects[key] = (
                        []
                        if es_items["hits"]["total"]["value"] == 0
                        else responder["function"](es_items["hits"]["hits"])
                    )
                else:
                    assets_key_objects[key] = (
                        session.query(orm_type)
                        .filter(orm_type.id.in_(assets_key_ids[key]))
                        .all()
                    )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={"content-type": "application/json"},
        content=jsonable_encoder(assets_key_objects),
    )
