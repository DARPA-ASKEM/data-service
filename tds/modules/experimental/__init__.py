"""
    TDS Experimental Module.

    A simple REST module that creates the basic endpoints for an entity in
    Terarium Data Service (TDS).
"""
from tds.modules.experimental.controller import experimental_router as router

ROUTE_PREFIX = "experimental"
TAGS = ["Experimental"]
