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

    def dynamic_relationship_direction(self, direction):
        """
        get direction of relationship based on direction type
        """
        if direction == "all":
            return "-[*]-"
        if direction == "child":
            return "<-[*]-"
        if direction == "parent":
            return "-[*]->"
        raise Exception("relationship direction is not allowed.")

    def connected_nodes_by_direction(self, payload, direction):
        """
        Connect nodes
        """
        with self.graph_db.session() as session:

            query = (
                f"Match (n1: {payload.get('root_type')}) "
                + f"{self.dynamic_relationship_direction(direction=direction)}(n2)"
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
        if root_type == "publication":
            return (
                "Match (m:model)-[r *1..]->(i:intermediate)-[r2:EXTRACTED_FROM]->"
                + f"(n:{root_type})"
            )
        if root_type == "intermediate":
            return (
                "Match (m:model)-[r *1..]->(md:model_revision)-[r2:REINTERPRETS]->"
                + f"(n:{root_type})"
            )
        raise Exception(f"Models can not be derived from this type: {root_type}")

    def derived_models(self, payload):
        """
        Return models derived from artifact
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

    def parent_model_revisions(self, payload):
        """
        Which model revisions help create the latest model id
        """
        with self.graph_db.session() as session:
            if payload.get("root_type") != "model":
                raise Exception("This search only allows root_type of type model")

            query = (
                "Match(mr:model_revision)<-[r:BEGINS_AT]-(m:model) "
                + "Where(m.id=$root_id) "
                + "Match (mr2:model_revision)<-[r2 *1.. ]-(mr) "
                + "With collect(mr)+collect(mr2) as mrs "
                + "Unwind mrs as both_rms "
                + "RETURN labels(both_rms) as label, both_rms.id as id "
            )
            response = session.run(query, root_id=payload.get("root_id"))

            return [
                {"label": res.data().get("label")[0], "id": res.data().get("id")}
                for res in response
            ]
