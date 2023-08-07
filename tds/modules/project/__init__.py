"""
    TDS Project Module.

    A simple REST module that creates the basic endpoints for an entity in
    Terarium Data Service (TDS).
"""
from tds.modules.project.controller import project_router as router

ROUTE_PREFIX = "projects"
TAGS = ["Project"]
