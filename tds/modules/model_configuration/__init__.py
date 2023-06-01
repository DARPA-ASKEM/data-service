"""
Model Configuration Module for TDS.
"""
from tds.modules.model_configuration.controller import (
    model_configuration_router as router,
)

ROUTE_PREFIX = "model_configurations"
TAGS = ["Model Configuration"]
