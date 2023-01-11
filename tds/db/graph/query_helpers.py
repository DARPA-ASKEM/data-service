"""
Helper functions
"""
from fastapi import HTTPException

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
        status_code=400, detail="Relationship direction is not allowed."
    )


def derived_models_query_generater(root_type: schema.ProvenanceType, root_id):
    """
    return all models, model revisions
    (sometimes intermediates) that were derived from a publication or intermediate
    """
    if root_type == "Publication":
        return f"""
            Match(Pu:Publication {{id:{root_id}}})
            <-[r:EXTRACTED_FROM]-(In:Intermediate) 
            Optional Match (In)<-[r2:REINTERPRETS *1..]-(Mr:ModelRevision) 
            Optional Match(Mr)
            -[r3:EDITED_FROM|COPIED_FROM|GLUED_FROM|STRATIFED_FROM  *1..]-
            (Mr2:ModelRevision) 
            with *,collect(r)+collect(r2)+collect(r3) as r4, 
            collect(Mr)+collect(Mr2) as ms 
            unwind ms as mss 
            unwind r4 as r5 
            Optional Match(mss)<-[r6:BEGINS_AT]-(Md:Model) 
            with *, collect(r5)+collect(r6) as r7 
            unwind r7 as r8 
            return Pu, In, ms,Md, r8
            """
    if root_type == "Intermediate":
        return f"""
            Match (In:Intermediate {{id:{root_id}}})<-[r2:REINTERPRETS *1..]
            -(Mr:ModelRevision) 
            Optional Match(Mr)
            -[r3:EDITED_FROM|COPIED_FROM|GLUED_FROM|STRATIFED_FROM  *1..]-
            (Mr2:ModelRevision) 
            with *,collect(r2)+collect(r3) as r4, collect(Mr)+collect(Mr2) as ms 
            unwind ms as mss 
            unwind r4 as r5 
            Optional Match(mss)<-[r6:BEGINS_AT]-(Md:Model) 
            with *, collect(r5)+collect(r6) as r7 
            unwind r7 as r8 
            return  In, ms,Md, r8
            """
    raise HTTPException(
        status_code=400, detail=f"Models can not be derived from this type: {root_type}"
    )


def parent_model_query_generator(root_type: schema.ProvenanceType, root_id):
    """
    Return match query to ModelRevision depending on root_type
    """
    match_node = match_node_builder(node_type=root_type, node_id=root_id)
    relationships_str = relationships_array_as_str(
        exclude=["CONTAINS", "IS_CONCEPT_OF"]
    )
    model_revision_node = node_builder(node_type=schema.ProvenanceType.ModelRevision)
    query_templates_index = {
        schema.ProvenanceType.Model: f"-[r:BEGINS_AT]->{model_revision_node} ",
        schema.ProvenanceType.Plan: f"-[r:USES]->{model_revision_node} ",
        schema.ProvenanceType.SimulationRun: ""
        + f"-[r:{relationships_str} *1..]->{model_revision_node} ",
        schema.ProvenanceType.Dataset: ""
        + f"-[r:{relationships_str} *1..]->{model_revision_node} ",
    }
    return match_node + query_templates_index[root_type]


def match_node_builder(node_type: schema.ProvenanceType = None, node_id=None):
    """
    return node with match statement
    """
    if node_type is None:
        return "Match(n) "
    node_type_character = return_node_abbr(node_type)
    if node_id is None:
        return f"Match ({node_type_character}:{node_type})"
    return f"Match ({node_type_character}:{node_type}  {{id: {node_id}}}) "


def return_node_abbr(root_type: schema.ProvenanceType):
    """
    Return node type abbr
    """
    return provenance_type_to_abbr[root_type]


def relationships_array_as_str(exclude=None, include=None):
    """
    Return relationships as pipe string
    """
    relationship_str = ""
    if exclude is not None:
        for type_ in schema.RelationType:
            value = type_.value
            if value in exclude:
                continue
            relationship_str += value + "|"
        return relationship_str[:-1]
    for type_ in schema.RelationType:
        value = type_.value
        if value in include:
            relationship_str += value + "|"
    return relationship_str[:-1]


def node_builder(node_type: schema.ProvenanceType = None, node_id=None):
    """
    Return node
    """
    if node_type is None:
        return "(n) "
    node_type_abbr = return_node_abbr(node_type)
    if node_id is None:
        return f" ({node_type_abbr}:{node_type})"
    return f"({node_type_abbr}:{node_type}  {{id: {node_id}}}) "


def nodes_edges(response=None):
    """
    Return nodes and edges
    """
    data = {"edges": [], "nodes": []}
    for relationship in response.graph().relationships:
        try:
            (start_label,) = relationship.__dict__.get("_start_node").__dict__.get(
                "_labels"
            )
            start_id = (
                relationship.__dict__.get("_start_node")
                .__dict__.get("_properties")
                .get("id")
            )
        except ValueError:
            continue

        try:
            (end_label,) = relationship.__dict__.get("_end_node").__dict__.get(
                "_labels"
            )
            end_id = (
                relationship.__dict__.get("_end_node")
                .__dict__.get("_properties")
                .get("id")
            )

        except ValueError:
            continue
        data["edges"].append(
            {
                "relationship": relationship.type,
                "left": {"type": start_label, "id": start_id},
                "right": {"type": end_label, "id": end_id},
            }
        )

    for node in response.graph().nodes:
        try:
            (node_label,) = node.__dict__.get("_labels")
            node_id = node.__dict__.get("_properties").get("id")
            uuid = build_uuid(node_label.lower(), str(node_id))

        except ValueError:
            continue
        data["nodes"].append({"type": node_label, "id": node_id, "uuid": uuid})
    return data


def build_uuid(label, id):
    """
    build uuid
    """
    label = label.lower()
    if label == "intermediate":
        path = "model/" + label.lower() + "s/" + str(id)
    if label == "modelparameter":
        path = "model/" + label.lower() + "s/" + str(id)
    if label == "simulationrun":
        path = "simulations/" + "runs/" + str(id)
    if label == "plan":
        path = "simulations/" + "plans/" + str(id)
    if label == "simulationparameter":
        path = "simulations/" + "simulationparameters/" + str(id)
    if label == "modelrevisions":
        path = None
    else:
        path = label.lower() + "s/" + str(id)
    return path
