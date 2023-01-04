"""
Import provenance handler
"""
from tds.db.graph.provenance_handler import ProvenanceHandler
from tds.db.graph.query_helpers import (
    derived_models_query_generater,
    dynamic_relationship_direction,
    parent_model_query_generator,
)


class SearchProvenance(ProvenanceHandler):
    """
    Search Provenance
    """

    def __init__(self, rdb, graph_db):
        super().__init__(rdb=rdb, graph_db=graph_db)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def connected_nodes_by_direction(self, payload, direction):
        """
        Connect nodes
        """
        with self.graph_db.session() as session:
            relation_direction = dynamic_relationship_direction(
                direction=direction, relationship_type="*"
            )
            query = (
                f"Match (n1: {payload.get('root_type')}) "
                + f"{relation_direction}(n2)"
                + "Where n1.id = $root_id "
                + "RETURN labels(n2) as label, n2.id as id"
            )

            response = session.run(query, root_id=payload.get("root_id"))

            response_data = [
                {res.data().get("label")[0]: res.data().get("id")} for res in response
            ]

            return sorted(response_data, key=lambda i: list(i.keys()))

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

    def derived_models(self, payload):
        """
        Return models derived from artifact (Publication or Intermediate)
        """
        with self.graph_db.session() as session:

            query = (
                f" {derived_models_query_generater(payload.get('root_type'))} "
                + "Where n.id = $root_id "
                + "RETURN labels(m) as label, m.id as id"
            )
            response = session.run(query, root_id=payload.get("root_id"))

            response_data = [
                {res.data().get("label")[0]: res.data().get("id")} for res in response
            ]

            return sorted(response_data, key=lambda i: list(i.keys()))

    def parent_model_revisions(self, payload):
        """
        Which model revisions help create the latest model id
        """
        with self.graph_db.session() as session:
            # if payload.get("root_type") != "Model":
            #     raise Exception("This search only allows root_type of type model")
            match_pattern = parent_model_query_generator(
                payload.get("root_type"), payload.get("root_id")
            )
            print(match_pattern)

            query = (
                f"{match_pattern}"
                + "Match (mr2:Model_revision)-[r2 *1.. ]->(mr) "
                + "With collect(mr)+collect(mr2) as mrs "
                + "Unwind mrs as both_rms "
                + "With DISTINCT both_rms "
                + "RETURN labels(both_rms) as label, both_rms.id as id "
            )

            response = session.run(
                query,
                root_id=payload.get("root_id"),
                root_type=payload.get("root_type"),
            )

            ## if response is empty there is only one version of the model. Return just that node.
            if len(response.data()) == 0:
                query = f"{match_pattern}" + "RETURN labels(mr) as label, mr.id as id "
                response = session.run(
                    query,
                    root_id=payload.get("root_id"),
                    root_type=payload.get("root_type"),
                )

            response_data = [
                {res.data().get("label")[0]: res.data().get("id")} for res in response
            ]

            return sorted(response_data, key=lambda i: list(i.keys()))

    def model_to_primative(self, payload):
        """
        Which models relay on which primatives
        """
        with self.graph_db.session() as session:
            query = (
                "match(i:Intermediate)<-[r *1..]-(m:Model)"
                "return i as Intermediate, r as relationship, m as Model"
            )
            response = session.run(query)

            return [
                {
                    "Intermediate": res.data().get("Intermediate").get("id"),
                    "Model": res.data().get("Model").get("id"),
                }
                for res in response
            ]

    def artifacts_created_by_user(self, payload):
        """
        Which nodes were created by user with id of ...
        """
        with self.graph_db.session() as session:
            query = (
                "match(n)-[r]->(n2) "
                + f"where r.user_id={payload.get('user_id')} "
                + "With collect(n)+collect(n2) as nodes "
                + "Unwind nodes as both_nodes "
                + "With DISTINCT both_nodes "
                + "RETURN labels(both_nodes) as label, both_nodes.id as id "
            )
            response = session.run(query)
            response_data = [
                {res.data().get("label")[0]: res.data().get("id")} for res in response
            ]

            return sorted(response_data, key=lambda i: list(i.keys()))
