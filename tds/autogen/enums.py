# pylint: skip-file
"""
Basic data Enums.
Skipping linter to prevent class docstring errors.
"""
from enum import Enum


class Direction(str, Enum):
    input = "input"
    output = "output"


class ExtractedType(str, Enum):
    equation = "equation"
    figure = "figure"
    table = "table"


class ModelOperations(str, Enum):
    copy = "copy"
    decompose = "decompose"
    glue = "glue"
    stratify = "stratify"


class OntologicalField(str, Enum):
    obj = "obj"
    unit = "unit"


class ProvenanceType(str, Enum):
    Concept = "Concept"
    Dataset = "Dataset"
    Model = "Model"
    ModelConfiguration = "ModelConfiguration"
    Project = "Project"
    Publication = "Publication"
    Simulation = "Simulation"
    Artifact = "Artifact"


class ProvenanceSearchTypes(str, Enum):
    artifacts_created_by_user = "artifacts_created_by_user"
    child_nodes = "child_nodes"
    concept = "concept"
    concept_counts = "concept_counts"
    connected_nodes = "connected_nodes"
    derived_models = "derived_models"
    parent_model_revisions = "parent_model_revisions"
    parent_models = "parent_models"
    parent_nodes = "parent_nodes"


class RelationType(str, Enum):
    BEGINS_AT = "BEGINS_AT"
    CITES = "CITES"
    COMBINED_FROM = "COMBINED_FROM"
    CONTAINS = "CONTAINS"
    COPIED_FROM = "COPIED_FROM"
    DECOMPOSED_FROM = "DECOMPOSED_FROM"
    DERIVED_FROM = "DERIVED_FROM"
    EDITED_FROM = "EDITED_FROM"
    EQUIVALENT_OF = "EQUIVALENT_OF"
    EXTRACTED_FROM = "EXTRACTED_FROM"
    GENERATED_BY = "GENERATED_BY"
    GLUED_FROM = "GLUED_FROM"
    IS_CONCEPT_OF = "IS_CONCEPT_OF"
    PARAMETER_OF = "PARAMETER_OF"
    REINTERPRETS = "REINTERPRETS"
    STRATIFIED_FROM = "STRATIFIED_FROM"
    USES = "USES"


class ResourceType(str, Enum):
    datasets = "datasets"
    model_configurations = "model_configurations"
    models = "models"
    publications = "publications"
    simulations = "simulations"
    workflows = "workflows"
    artifacts = "artifacts"


class Role(str, Enum):
    author = "author"
    contributor = "contributor"
    maintainer = "maintainer"
    other = "other"


class TaggableType(str, Enum):
    datasets = "datasets"
    features = "features"
    model_configurations = "model_configurations"
    model_parameters = "model_parameters"
    models = "models"
    projects = "projects"
    publications = "publications"
    qualifiers = "qualifiers"
    simulations = "simulations"
    artifacts = "artifacts"


class ValueType(str, Enum):
    binary = "binary"
    bool = "bool"
    float = "float"
    int = "int"
    str = "str"


class SimulationEngine(str, Enum):
    sciml = "sciml"
    ciemss = "ciemss"


class SimulationType(str, Enum):
    calibration = "calibration"
    calibration_simulation = "calibration_simulation"
    ensemble = "ensemble"
    simulation = "simulation"


class SimulationStatus(str, Enum):
    cancelled = "cancelled"
    complete = "complete"
    error = "error"
    queued = "queued"
    running = "running"
