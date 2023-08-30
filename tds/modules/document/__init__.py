"""
    TDS Document Module.

    A simple REST module that creates the basic endpoints for an entity in
    Terarium Data Service (TDS).
"""
from tds.modules.document.controller import document_router as router

ROUTE_PREFIX = "documents"
TAGS = ["Document"]
