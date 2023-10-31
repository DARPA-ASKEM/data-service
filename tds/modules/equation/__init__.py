"""
    TDS Equation Module.

    A simple REST module that creates the basic endpoints for an entity in
    Terarium Data Service (TDS).
"""
from tds.modules.equation.controller import equation_router as router

ROUTE_PREFIX = "equations"
TAGS = ["Equations"]
