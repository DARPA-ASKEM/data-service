"""
TDS Workflow Model Definition.
"""

from typing import List, Optional

from pydantic import BaseModel, Enum

from tds.db.base import BaseElasticSearchModel
from tds.settings import settings


class Transform(BaseModel):
    x: float
    y: float
    k: Optional[float]


class State(BaseModel):
    modelId: Optional[str]
    modelConfigurationIds: List[str] = []


class OperationType(str, Enum):
    ModelOperation = "ModelOperation"
    Dataset = "Dataset"
    CalibrationOperationCiemss = "CalibrationOperationCiemss"
    SimulateCiemssOperation = "SimulateCiemssOperation"
    CalibrateEnsembleCiemms = "CalibrateEnsembleCiemms"
    SimulateEnsembleCiemss = "SimulateEnsembleCiemss"
    CalibrationOperationJulia = "CalibrationOperationJulia"
    SimulateJuliaOperation = "SimulateJuliaOperation"
    CalibrateEnsembleJulia = "CalibrateEnsembleJulia"
    SimulateEnsembleJulia = "SimulateEnsembleJulia"


class Output(BaseModel):
    id: str
    type: str
    label: str
    value: List[str]
    status: str


class Input(BaseModel):
    id: str
    type: str
    label: str
    status: str
    value: List[str]
    acceptMultiple: bool


class Node(BaseModel):
    id: str
    workflowId: str
    operationType: OperationType
    displayName: str
    x: int
    y: int
    state: State
    inputs: List[Input]
    outputs: List[Output]
    statusCode: str
    width: int
    height: int


class Edge(BaseModel):
    id: str
    workflowId: str
    source: str
    sourcePortId: str
    target: str
    targetPortId: str
    points: List[Transform]


class Workflow(BaseElasticSearchModel):
    """
    Workflow Data Model
    """

    id: str
    name: str
    description: Optional[str]
    transform: Transform
    nodes: List[Node] = []
    edges: List[Edge] = []

    _index = "workflow"

    def save(self):
        """
        Method saves the object to ElasticSearch.
        """
        res = super().save()
        if settings.NEO4J_ENABLED:
            self._establish_provenance()
        return res

    def _extract_concepts(self):
        pass

    def _establish_provenance(self):
        pass

    class Config:
        """
        Workflow Data Model Swagger Example
        """

        schema_extra = {
            "example": {
                "name": "Test Workflow",
                "description": "This is the description",
                "transform": {
                    "x": 127.0002,
                    "y": 17.1284,
                    "z": 2.53,
                },
                "nodes": [
                    {
                        "model": {
                            "id": "model_id",
                            "configurations": [{"id": "model_configuration_id"}],
                        }
                    }
                ],
                "edges": [],
            }
        }
