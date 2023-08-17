"""
TDS Project helpers.
"""
from collections import defaultdict
from typing import Dict, List

from sqlalchemy.orm import Session

from tds.db import entry_exists, es_client, rdb
from tds.lib.utils import get_singular_index
from tds.modules.artifact.response import artifact_response
from tds.modules.code.response import code_response
from tds.modules.dataset.response import dataset_response
from tds.modules.model.utils import model_list_fields, model_list_response
from tds.modules.model_configuration.response import configuration_response
from tds.modules.project.model import Project, ProjectAsset
from tds.modules.simulation.response import simulation_response
from tds.modules.workflow.response import workflow_response
from tds.schema.resource import ResourceType, get_resource_orm
from tds.settings import settings

es_list_response = {
    ResourceType.models: {"function": model_list_response, "fields": model_list_fields},
    ResourceType.model_configurations: {
        "function": configuration_response,
        "fields": None,
    },
    ResourceType.datasets: {"function": dataset_response, "fields": None},
    ResourceType.simulations: {"fields": None, "function": simulation_response},
    ResourceType.workflows: {"fields": None, "function": workflow_response},
    ResourceType.artifacts: {"fields": None, "function": artifact_response},
    ResourceType.code: {"fields": None, "function": code_response},
}

es_resources = [
    ResourceType.datasets,
    ResourceType.models,
    ResourceType.model_configurations,
    ResourceType.simulations,
    ResourceType.workflows,
    ResourceType.artifacts,
    ResourceType.code,
]


class ResourceDoesNotExist(Exception):
    """
    ResourceDoesNotExist Exception class.
    """

    message = "The Requested Resource does not exist."

    def __init__(self, resource_type):
        self.message = f"{resource_type}: {self.message}"


def save_project(project: dict, session):
    """
    Function saves the project from a payload dict.
    """
    asset_dict = project.pop("assets")
    assets = check_assets(assets=asset_dict)

    if assets:
        project = Project(**project)
        session.add(project)
        session.commit()
        build_asset_records(
            project_id=project.id, asset_ids=asset_dict, session=session
        )
        session.commit()
    return project


def check_assets(assets: list) -> bool:
    """
    Function verifies assets exist before saving the project.
    """
    for resource_type in assets:
        if resource_type in es_resources:
            resources = handle_es_resource(
                object_resource=resource_type, object_ids=assets[resource_type]
            )
        else:
            resources = handle_orm_resource(
                object_resource=resource_type, object_ids=assets[resource_type]
            )

        if resources is False:
            raise ResourceDoesNotExist(resource_type)

    return True


def handle_es_resource(object_resource: str, object_ids: list):
    """
    Function handles an ElasticSearch asset resource.
    """
    es = es_client()
    index = get_singular_index(f"{settings.ES_INDEX_PREFIX}{object_resource}")
    query = {"ids": {"values": object_ids}}
    res = es.search(index=index, query=query)

    if int(res["hits"]["total"]["value"]) != len(object_ids):
        return False

    return True


def handle_orm_resource(object_resource: ResourceType, object_ids: list):
    """
    Function handles ORM project assets.
    """
    current_orm = get_resource_orm(object_resource)
    if not all((entry_exists(rdb.connect(), current_orm, oid) for oid in object_ids)):
        raise ResourceDoesNotExist(object_resource)
    return True


def build_asset_records(project_id, asset_ids, session):
    """
    Function builds the asset record list and saves it to the DB.
    """
    for resource_type in asset_ids:
        resource_ids = asset_ids[resource_type]
        project_assets = [
            ProjectAsset(
                project_id=project_id,
                resource_id=resource_id,
                resource_type=resource_type,
                external_ref="",
            )
            for resource_id in resource_ids
        ]
        session.bulk_save_objects(project_assets)


def adjust_project_assets(
    project_id: int, assets: Dict[ResourceType, List[int]], session: Session
):
    """
    Add new entries and remove unused entries
    """
    active = defaultdict(list)
    for asset in session.query(ProjectAsset).filter(
        ProjectAsset.project_id == project_id
    ):
        active[asset.resource_type].append(asset.resource_id)

    for resource_type, resource_ids in assets.items():
        project_assets = [
            ProjectAsset(
                project_id=project_id,
                resource_id=resource_id,
                resource_type=resource_type,
                external_ref="",
            )
            for resource_id in resource_ids
            if resource_id not in active[resource_type]
        ]
        session.bulk_save_objects(project_assets)

    for resource_type, resource_ids in active.items():
        inactive_ids = set(resource_ids) - set(assets.get(resource_type, []))
        for inactive_id in inactive_ids:
            session.delete(session.query(ProjectAsset).get(inactive_id))
