"""
Project-specific logic
"""

from collections import defaultdict
from logging import Logger
from typing import Dict, List

from sqlalchemy.orm import Session

from tds.db.enums import ResourceType
from tds.modules.project.model import ProjectAsset

logger = Logger(__file__)


def save_project_assets(
    project_id: int, assets: Dict[ResourceType, List[int]], session: Session
):
    """
    Save project assets to relational DB
    """
    for resource_type, resource_ids in assets.items():
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
        for id in inactive_ids:
            session.delete(session.query(ProjectAsset).get(id))


def clean_up_asset_return(project_assets):
    return_obj = {}
    for asset in project_assets:
        if asset.resource_type not in return_obj:
            return_obj[asset.resource_type] = []
        return_obj[asset.resource_type].append(asset.resource_id)

    return return_obj
