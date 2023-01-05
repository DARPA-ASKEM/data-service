"""
Import provenance handler
"""
import logging
from collections import defaultdict

from fastapi import FastAPI, HTTPException

from tds.autogen import schema
from tds.db.graph.provenance_handler import ProvenanceHandler
from tds.db.graph.query_helpers import (
    derived_models_query_generater,
    dynamic_relationship_direction,
    match_node_builder,
    node_builder,
    parent_model_query_generator,
    relationships_array_as_str,
)
from tds.schema.provenance import provenance_type_to_abbr


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
            # return string of relationship excluding CONTAINS and IS_CONCEPT_OF
            relationships_str = relationships_array_as_str(
                exclude=["CONTAINS", "IS_CONCEPT_OF"]
            )

            # set the direction of the search dynamically
            relation_direction = dynamic_relationship_direction(
                direction=direction, relationship_type=f"r:{relationships_str} *1.."
            )

            # build the first match node
            match_node = match_node_builder(
                node_type=payload.get("root_type"), node_id=payload.get("root_id")
            )

            # build the query. n is an arbitrary node
            query = (
                f"{match_node}"
                + f"{relation_direction}(n) "
                + "With DISTINCT n "
                + "RETURN labels(n) as label, n.id as id"
            )
            print(query)
            logging.info(query)

            response = session.run(query)

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
        if payload.get("root_type") not in ("Publication", "Intermediate"):
            raise HTTPException(
                status_code=404,
                detail="Derived models can only be found from root types of Publication or Intermediates",
            )

        with self.graph_db.session() as session:

            query = (
                f" {derived_models_query_generater(root_type=payload.get('root_type'), root_id=payload.get('root_id'))} "
                + "RETURN labels(Md) as label, Md.id as id"
            )
            response = session.run(query)

            response_data = [
                {res.data().get("label")[0]: res.data().get("id")} for res in response
            ]

            return sorted(response_data, key=lambda i: list(i.keys()))

    def parent_model_revisions(self, payload):
        """
        Which model revisions help create the latest model which was used to create the artifact
        """
        if payload.get("root_type") not in (
            "Model",
            "SimulationRun",
            "Plan",
            "Dataset",
        ):
            raise HTTPException(
                status_code=404,
                detail="Derived models can only be found from root types of Publication or Intermediates",
            )
        with self.graph_db.session() as session:

            match_pattern = parent_model_query_generator(
                payload.get("root_type"), payload.get("root_id")
            )
            relationships_str = relationships_array_as_str(
                exclude=["CONTAINS", "IS_CONCEPT_OF"]
            )

            query = (
                f"{match_pattern}"
                + f"Match (Mr2:ModelRevision)"
                + f"-[r2:{relationships_str} *1.. ]->(Mr) "
                + f"With collect(Mr)+collect(Mr2) as Mrs "
                + "Unwind Mrs as Both_rms "
                + "With DISTINCT Both_rms "
                + "RETURN labels(Both_rms) as label, Both_rms.id as id "
            )
            print("heee")
            print(query)

            response = session.run(query)
            response_data = [
                {res.data().get("label")[0]: res.data().get("id")} for res in response
            ]

            ## if response is empty there is only one version of the model. Return just that node.
            if len(response_data) == 0:
                print("here")
                query = f"{match_pattern}" + "RETURN labels(Mr) as label, Mr.id as id "
                response = session.run(query)
                response_data = [
                    {res.data().get("label")[0]: res.data().get("id")}
                    for res in response
                ]

            print(response_data)

            return sorted(response_data, key=lambda i: list(i.keys()))

    def parent_models(self, payload):
        """
        Which models help create the latest model
        """
        if payload.get("root_type") not in ("Model"):
            raise HTTPException(
                status_code=404,
                detail="Parent models can only be found from root types of Model, Plan, SimulationRun, Dataset",
            )
        with self.graph_db.session() as session:

            match_pattern = parent_model_query_generator(
                payload.get("root_type"), payload.get("root_id")
            )

            model_relationships = relationships_array_as_str(
                include=[
                    "EDITED_FROM",
                    "COPIED_FROM",
                    "GLUED_FROM",
                    "DECOMPOSED_FROM",
                    "STRATIFIED_FROM",
                ]
            )

            query = (
                match_pattern
                + f"Match (Mr)-[:{model_relationships} *1..]->(Mr2:ModelRevision)"
                + "With collect(Mr)+collect(Mr2) as Mrs "
                + "Unwind Mrs as Both_rms "
                + "With DISTINCT Both_rms "
                + "Match (md2:Model)-[:BEGINS_AT]->(Both_rms) "
                + "Return labels(md2) as label, md2.id as id"
            )
            response = session.run(query)
            response_data = [
                {res.data().get("label")[0]: res.data().get("id")} for res in response
            ]

            return sorted(response_data, key=lambda i: list(i.keys()))

    def model_to_primative(self, payload):
        """
        Which models relay on which primatives
        """
        with self.graph_db.session() as session:
            match_node = match_node_builder(
                node_type=schema.ProvenanceType.Intermediate
            )

            query = (
                f"{match_node}<-[r *1..]-{node_builder(node_type='Model')}"
                "return In as Intermediate, r as relationship, Md as Model"
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
            match_node = match_node_builder()
            query = (
                f"{match_node}-[r]->(n2) "
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

    def concept(self, payload):
        """
        Which nodes are associated with a concept ...
        """
        with self.graph_db.session() as session:
            match_node = match_node_builder(node_type="Concept")
            query = (
                match_node
                + "-[r:IS_CONCEPT_OF]->(n) "
                + f"Where Cn.concept='{payload.get('concept')}' "
                + "return labels(n) as label, n.id as id"
            )
            response = session.run(query)
            response_data = [
                {res.data().get("label")[0]: res.data().get("id")} for res in response
            ]

            return sorted(response_data, key=lambda i: list(i.keys()))

    def concept_counts(self, payload):
        """
        Counts of which nodes are associated with a concept
        """
        with self.graph_db.session() as session:
            match_node = match_node_builder(node_type="Concept")
            query = (
                match_node
                + "-[r:IS_CONCEPT_OF]->(n) "
                + f"Where Cn.concept='{payload.get('concept')}' "
                + "return labels(n) as label, n.id as id"
            )
            response = session.run(query)
            response_data = [
                {res.data().get("label")[0]: res.data().get("id")} for res in response
            ]

            counts = defaultdict(int)
            for response in response_data:
                print(response)
                print(counts)
                for key in response:
                    counts[key] += 1
        return counts
