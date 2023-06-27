"""
    TDS Artifact Module.

    A simple REST module that creates the basic endpoints for an entity in
    Terarium Data Service (TDS).
"""
from tds.modules.artifact.controller import artifact_router as router

ROUTE_PREFIX = "artifacts"
TAGS = ["Artifact"]
