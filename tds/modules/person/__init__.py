"""
    TDS Person Module.

    A simple REST module that creates the basic endpoints for an entity in
    Terarium Data Service (TDS).
"""
from tds.modules.person.controller import person_router as router

ROUTE_PREFIX = "persons"
TAGS = ["Person"]
