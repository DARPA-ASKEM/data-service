"""
    TDS Provenance Module.

    A simple REST module that creates the basic endpoints for an entity in
    Terarium Data Service (TDS).
"""
from tds.modules.provenance.controller import provenance_router as router

ROUTE_PREFIX = "provenance_new"
TAGS = ["Provenance"]
