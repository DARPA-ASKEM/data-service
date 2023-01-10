from fastapi import FastAPI, HTTPException

from tds.autogen import schema
from tds.schema.provenance import provenance_type_to_abbr


def dynamic_relationship_direction(direction, relationship_type):
    """
    return direction of relationship based on direction type.
    allow for different relationship types
    """
    if direction == "all":
        return f"-[{relationship_type}]-"
    if direction == "child":
        return f"<-[{relationship_type}]-"
    if direction == "parent":
        return f"-[{relationship_type}]->"
    raise HTTPException(
        status_code=404, detail="Relationship direction is not allowed."
    )


def derived_models_query_generater(root_type: schema.ProvenanceType, root_id):
    """
    Return match query for models derived from a publication or intermediate
    """
    root_node = node_builder(node_type=root_type, node_id=root_id)
    match_node = match_node_builder(node_type=schema.ProvenanceType.Model)
    if root_type == "Publication":
        In_node = node_builder(node_type="Intermediate")
        return (
            match_node
            + f"-[r *1..]->"
            + f"{In_node}-[r2:EXTRACTED_FROM]->"
            + f"{root_node}"
        )
    if root_type == "Intermediate":

        Mr_node = node_builder(node_type="ModelRevision")
        return match_node + f"-[r *1..]->{Mr_node}-[r2:REINTERPRETS]->" + f"{root_node}"
    raise HTTPException(
        status_code=404, detail=f"Models can not be derived from this type: {root_type}"
    )


def parent_model_query_generator(root_type: schema.ProvenanceType, root_id):
    """
    Return match query to ModelRevision depending on root_type
    """
    try:
        match_node = match_node_builder(node_type=root_type, node_id=root_id)
        relationships_str = relationships_array_as_str(
            exclude=["CONTAINS", "IS_CONCEPT_OF"]
        )
        model_revision_node = node_builder(
            node_type=schema.ProvenanceType.ModelRevision
        )
        query_templates_index = {
            schema.ProvenanceType.Model: f"-[r:BEGINS_AT]->{model_revision_node} ",
            schema.ProvenanceType.Plan: f"-[r:USES]->{model_revision_node} ",
            schema.ProvenanceType.Simulation_run: f"-[r:{relationships_str} *1..]->{model_revision_node} ",
            schema.ProvenanceType.Dataset: f"-[r:{relationships_str} *1..]->{model_revision_node} ",
        }
        return match_node + query_templates_index[root_type]
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Search for model revisions is not available from this root type: {root_type}",
        )


def match_node_builder(node_type: schema.ProvenanceType = None, node_id=None):
    if node_type is None:
        return f"Match(n) "
    node_type_character = return_node_abbr(node_type)
    if node_id is None:
        return f"Match ({node_type_character}:{node_type})"
    return f"Match ({node_type_character}:{node_type}  {{id: {node_id}}}) "


def return_node_abbr(root_type: schema.ProvenanceType):
    return provenance_type_to_abbr[root_type].value


def relationships_array_as_str(exclude=[]):
    relationship_str = ""
    for type_ in schema.RelationType:
        value = type_.value
        if value in exclude:
            continue
        relationship_str += value + "|"
    return relationship_str[:-1]


def node_builder(node_type: schema.ProvenanceType = None, node_id=None):
    if node_type is None:
        return f"(n) "
    node_type_abbr = return_node_abbr(node_type)
    if node_id is None:
        return f" ({node_type_abbr}:{node_type})"
    return f"({node_type_abbr}:{node_type}  {{id: {node_id}}}) "
