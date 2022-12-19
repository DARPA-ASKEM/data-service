"""
Project-specific logic
"""

from collections import defaultdict
from logging import Logger
from typing import Dict, List

from sqlalchemy.orm import Session

from tds.autogen import orm, schema

logger = Logger(__file__)


def save_project_assets(
    project_id: int, assets: Dict[schema.ResourceType, List[int]], session: Session
):
    """
    Save project assets to relational DB
    """
    for resource_type, resource_ids in assets.items():
        project_assets = [
            orm.ProjectAsset(
                project_id=project_id,
                resource_id=resource_id,
                resource_type=resource_type,
                external_ref="",
            )
            for resource_id in resource_ids
        ]
        session.bulk_save_objects(project_assets)


def adjust_project_assets(
    project_id: int, assets: Dict[schema.ResourceType, List[int]], session: Session
):
    """
    Add new entries and remove unused entries
    """
    active = defaultdict(list)
    for asset in session.query(orm.ProjectAsset).filter(
        orm.ProjectAsset.project_id == project_id
    ):
        active[asset.resource_type].append(asset.resource_id)

    for resource_type, resource_ids in assets.items():
        project_assets = [
            orm.ProjectAsset(
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
            session.delete(session.query(orm.ProjectAsset).get(id))
