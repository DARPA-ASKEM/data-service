"""
Import provenance handler
"""
from tds.db.graph.provenance_handler import ProvenanceHandler


class SearchProvenance(ProvenanceHandler):
    """
    Search Provenance
    """

    def __init__(self, rdb, graph_db):
        super().__init__(rdb=rdb, graph_db=graph_db)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def dynamic_relationship_direction(self, direction, relationship_type):
        """
        get direction of relationship based on direction type
        """
        if direction == "all":
            return f"-[{relationship_type}]-"
        if direction == "child":
            return f"<-[{relationship_type}]-"
        if direction == "parent":
            return f"-[{relationship_type}]->"
        raise Exception("relationship direction is not allowed.")

    def connected_nodes_by_direction(self, payload, direction):
        """
        Connect nodes
        """
        with self.graph_db.session() as session:

            query = (
                f"Match (n1: {payload.get('root_type')}) "
                + f"{self.dynamic_relationship_direction(direction=direction, relationship_type='*')}(n2)"
                + "Where n1.id = $root_id "
                + "RETURN labels(n2) as label, n2.id as id"
            )

            response = session.run(query, root_id=payload.get("root_id"))

            return [
                {"label": res.data().get("label")[0], "id": res.data().get("id")}
                for res in response
            ]

    def connected_nodes(self, payload):
        """
        Return all connected nodes
        """
        return self.connected_nodes_by_direction(payload=payload, direction="all")

    def child_nodes(self, payload):
        """
        Return all child nodes
        """
        return self.connected_nodes_by_direction(payload=payload, direction="child")

    def parent_nodes(self, payload):
        """
        Return all parent nodes
        """
        return self.connected_nodes_by_direction(payload=payload, direction="parent")

    def derived_models_query_generater(self, root_type):
        """
        Return models derived from a publication or intermediate
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

    def derived_models(self, payload):
        """
        Return models derived from artifact (Publication or Intermediate)
        """
        with self.graph_db.session() as session:

            query = (
                f" {self.derived_models_query_generater(payload.get('root_type'))} "
                + "Where n.id = $root_id "
                + "RETURN labels(m) as label, m.id as id"
            )
            print(query)
            response = session.run(query, root_id=payload.get("root_id"))

            return [
                {"label": res.data().get("label")[0], "id": res.data().get("id")}
                for res in response
            ]

    def parent_model_query_generator(self, root_type, root_id):
        """
        Return query depending on root_type
        """
        if root_type == "Model":
            print("here")
            return (
                f"Match(m:{root_type}"
                + "{id:"
                + f"{root_id}"
                + "})-[r:BEGINS_AT]->(mr:Model_revision) "
            )
        if root_type == "Plan":
            return (
                f"Match(m:{root_type}"
                + "{id:"
                + f"{root_id}"
                + "})-[r:USES]->(mr:Model_revision) "
            )
        if root_type in ("Simulation_run", "Dataset"):
            return (
                f"Match(m:{root_type}"
                + "{id:"
                + f"{root_id}"
                + "})-[r *1..]->(mr:Model_revision) "
            )
        raise Exception(
            f"Search for model revision is not available from this root type: {root_type}"
        )

    def parent_model_revisions(self, payload):
        """
        Which model revisions help create the latest model id
        """
        with self.graph_db.session() as session:
            # if payload.get("root_type") != "Model":
            #     raise Exception("This search only allows root_type of type model")

            query = (
                f"{self.parent_model_query_generator(payload.get('root_type'),payload.get('root_id'))}"
                + "Match (mr2:Model_revision)-[r2 *1.. ]->(mr) "
                + "With collect(mr)+collect(mr2) as mrs "
                + "Unwind mrs as both_rms "
                + "With DISTINCT both_rms "
                + "RETURN labels(both_rms) as label, both_rms.id as id "
            )
            print(query)
            response = session.run(query, root_id=payload.get("root_id"))

            return [
                {"label": res.data().get("label")[0], "id": res.data().get("id")}
                for res in response
            ]
