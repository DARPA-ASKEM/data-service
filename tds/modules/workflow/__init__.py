"""
    TDS Workflow Module.

    A simple REST module that creates the basic endpoints for an entity in
    Terarium Data Service (TDS).
"""
from tds.modules.workflow.controller import workflow_router as router

ROUTE_PREFIX = "workflows"
TAGS = ["TDS Workflow"]
