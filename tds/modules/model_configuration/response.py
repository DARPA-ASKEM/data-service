"""
TDS Model Configuration Response object.
"""
from pydantic import BaseModel


class ModelConfigurationResponse(BaseModel):
    """
    Model Configuration Response Object.
    """

    id: str
    name: str
    description: str
    model_id: str
    model: object
    model_id: str
