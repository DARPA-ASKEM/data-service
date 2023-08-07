"""
    TDS External Module.

    A simple REST module that creates the basic endpoints for an entity in
    Terarium Data Service (TDS).
"""
from tds.modules.external.controller import external_router as router

ROUTE_PREFIX = "external"
TAGS = ["External"]
