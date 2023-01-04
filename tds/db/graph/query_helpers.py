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
    raise Exception("relationship direction is not allowed.")


def derived_models_query_generater(root_type):
    """
    Return match query for models derived from a publication or intermediate
    """
    if root_type == "Publication":
        return (
            "Match (m:Model)-[r *1..]->(i:Intermediate)-[r2:EXTRACTED_FROM]->"
            + f"(n:{root_type})"
        )
    if root_type == "Intermediate":
        return (
            "Match (m:Model)-[r *1..]->(md:Model_revision)-[r2:REINTERPRETS]->"
            + f"(n:{root_type})"
        )
    raise Exception(f"Models can not be derived from this type: {root_type}")


def parent_model_query_generator(root_type, root_id):
    """
    Return match query to Model_revision depending on root_type
    """
    try:
        query_templates_index = {
            "Model": f"Match(m: {root_type} {{id: {root_id}}})-[r:BEGINS_AT]->(mr:Model_revision) ",
            "Plan": f"Match(m: {root_type} {{id: {root_id}}})-[r:USES]->(mr:Model_revision) ",
            "Simulation_run": f"Match(m: {root_type}  {{id: {root_id}}})-[r *1..]->(mr:Model_revision) ",
            "Dataset": f"Match(m: {root_type}  {{id: {root_id}}})-[r *1..]->(mr:Model_revision) ",
        }
        return query_templates_index[root_type]
    except KeyError:
        raise Exception(
            f"Search for model revision is not available from this root type: {root_type}"
        )
