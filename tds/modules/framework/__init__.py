"""
    TDS Framework Module.

    A simple REST module that creates the basic endpoints for an entity in
    Terarium Data Service (TDS).
"""
from tds.modules.framework.controller import framework_router as router

ROUTE_PREFIX = "frameworks"
TAGS = ["Framework"]
