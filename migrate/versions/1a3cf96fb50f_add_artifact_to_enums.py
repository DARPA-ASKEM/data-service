"""Add artifact to enums.

Revision ID: 1a3cf96fb50f
Revises: 895deab7e80c
Create Date: 2023-06-14 19:38:18.828648

"""
import sqlalchemy as sa

# pylint: disable=no-member, invalid-name
from alembic import op

from migrate.scripts.enums import (
    provenance_type,
    resource_type,
    taggable_type,
    update_enum,
)

# revision identifiers, used by Alembic.
revision = "1a3cf96fb50f"
down_revision = "895deab7e80c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    resource_enums = {
        "association": "resource_type",
        "project_asset": "resource_type",
    }
    resource_list = [
        "datasets",
        "models",
        "model_configurations",
        "publications",
        "simulations",
        "workflows",
        "artifacts",
    ]
    update_enum(
        name="resourcetype",
        enum_obj=resource_type,
        cols=resource_enums,
        enum_entities=resource_list,
    )
    taggable_enums = {
        "ontology_concept": "type",
    }
    taggable_list = [
        "datasets",
        "models",
        "projects",
        "publications",
        "qualifiers",
        "simulation_parameters",
        "model_configurations",
        "simulations",
        "workflows",
        "artifacts",
    ]
    update_enum(
        name="taggabletype",
        enum_obj=taggable_type,
        cols=taggable_enums,
        enum_entities=taggable_list,
    )
    provenance_enums = {
        "provenance": ["left_type", "right_type"],
    }
    provenance_list = [
        "Concept",
        "Dataset",
        "Model",
        "ModelConfiguration",
        "Project",
        "Publication",
        "Simulation",
        "Artifact",
    ]
    update_enum(
        name="provenancetype",
        enum_obj=provenance_type,
        cols=provenance_enums,
        enum_entities=provenance_list,
    )


def downgrade() -> None:
    pass
