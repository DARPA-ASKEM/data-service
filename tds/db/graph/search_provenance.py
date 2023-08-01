"""
Import provenance handler
"""
import logging
from collections import defaultdict
from typing import Optional

from fastapi import HTTPException
from neo4j import Driver
from sqlalchemy.engine.base import Engine

from tds.db.graph.query_helpers import (
    derived_models_query_generater,
    dynamic_relationship_direction,
    match_node_builder,
    nodes_edges,
    parent_model_query_generator,
    relationships_array_as_str,
)
from tds.schema.provenance import provenance_type_to_abbr


class SearchProvenance:
    """
    Search Provenance
    """

    def __init__(self, rdb: Engine, graph_db: Optional[Driver] = None):
        self.__connection__ = rdb.connect()
        self.graph_db = graph_db

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def model_publication(self, payload):
        """
        find publication that was extracted to create model
        """
        with self.graph_db.session() as session:
            query = (
                f"Match (Md:Model {{id:'{payload.get('root_id')}'}})"
                "<-[r:REINTERPRETS|EXTRACTED_FROM|BEGINS_AT *1..]->"
                "(Pu:Publication) return Pu"
            )

            response = session.run(query)
            results = list(response.data())
            if len(results) == 0:
                return None
            return results[0]["Pu"]

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

            node_abbr = provenance_type_to_abbr[payload.get("root_type")]

            query = (
                f"{match_node}"
                + f"{relation_direction}(n) "
                # + "With DISTINCT n "
                + f"return {node_abbr}, r, n"
            )

            logging.info(query)
            response = session.run(query)

            return nodes_edges(response=response)

    def connected_nodes(self, payload):
        """
        Return all connected nodes
        """
        with self.graph_db.session() as session:
            match_node = match_node_builder(
                payload.get("root_type"), payload.get("root_id")
            )
            node_abbr = provenance_type_to_abbr[payload.get("root_type")]

            def set_max_level(hops):
                if hops is not None:
                    return f"maxLevel: {hops}, "
                return ""

            def set_limit_level(limit):
                return f"limit: {limit} "

            relationships_str = relationships_array_as_str(
                exclude=["CONTAINS", "IS_CONCEPT_OF"]
            )
            query = (
                f"{match_node} CALL apoc.path.subgraphAll({node_abbr}, "
                + "{"
                + f'relationshipFilter: "{relationships_str}",'
                + "minLevel: 0, "
                + f"{set_limit_level(payload.get('limit',-1))}, "
                f"{set_max_level(payload.get('hops',None))}"
                + """
                whitelistNodes: []
                })
                YIELD nodes, relationships
                RETURN nodes, relationships
                """
            )
            response = session.run(query)
            return nodes_edges(
                response=response,
                nodes=payload.get("nodes", True),
                edges=payload.get("edges", False),
                types=payload.get("types"),
                versions=payload.get("versions"),
            )

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
                status_code=400,
                detail="Derived models can only be found from "
                + "root types of Publication or Intermediates",
            )
        with self.graph_db.session() as session:
            generated_query = derived_models_query_generater(
                root_type=payload.get("root_type"), root_id=payload.get("root_id")
            )

            response = session.run(generated_query)

            return nodes_edges(response)

    def parent_model_revisions(self, payload):
        """
        Which model revisions help create the
        latest model which was used to create the artifact
        """
        if payload.get("root_type") not in (
            "Model",
            "SimulationRun",
            "Plan",
            "Dataset",
        ):
            raise HTTPException(
                status_code=400,
                detail="Derived models can only be found "
                + "from root types of Model, SimulationRun, Plan and Dataset",
            )
        with self.graph_db.session() as session:
            match_pattern = parent_model_query_generator(
                payload.get("root_type"), payload.get("root_id")
            )
            relationships_str = relationships_array_as_str(
                exclude=["CONTAINS", "IS_CONCEPT_OF"]
            )

            query = f"""
                {match_pattern}
                Optional Match (Mr2:ModelRevision)
                -[r2:{relationships_str} *1.. ]->(Mr) 
                With *,collect(r)+collect(r2) as r3,  
                collect(Mr)+collect(Mr2) as Mrs 
                Unwind Mrs as Both_rms 
                Unwind r3 as r4 
                with * 
                Optional Match(Both_rms)<-[r5:BEGINS_AT]-(Md:Model) 
                With *,collect(r4)+collect(r5) as r6 
                Unwind r6 as r7 
                RETURN Both_rms,Md,r7
                """
            response = session.run(query)
            return nodes_edges(response=response)

    def parent_models(self, payload):
        """
        Which models help create the latest model
        """
        if payload.get("root_type") not in (
            "Model",
            "Dataset",
            "SimulationRun",
            "Plan",
        ):
            raise HTTPException(
                status_code=400,
                detail="Parent models can only be found from root "
                + "types of Model, Plan, SimulationRun, Dataset",
            )
        with self.graph_db.session() as session:
            match_pattern = parent_model_query_generator(
                payload.get("root_type"), payload.get("root_id")
            )
            node_abbr = provenance_type_to_abbr[payload.get("root_type")]

            model_relationships = relationships_array_as_str(
                include=[
                    "EDITED_FROM",
                    "COPIED_FROM",
                    "GLUED_FROM",
                    "DECOMPOSED_FROM",
                    "STRATIFIED_FROM",
                ]
            )

            query = f"""
                {match_pattern} 
                Optional Match (Mr)-[r2:{model_relationships} *1..]->(Mr2:ModelRevision)
                With *, collect(Mr)+collect(Mr2) as Mrs,collect(r)+collect(r2) as r3
                Unwind Mrs as Both_rms 
                with *
                Optional Match (md2:Model)-[r4:BEGINS_AT]->(Both_rms) 
                with *,  collect(r3)+collect(r4)as r5
                Return {node_abbr},md2,Both_rms,r5
                """

            response = session.run(query)
            return nodes_edges(response=response)

            # response_data = [
            #     {res.data().get("label")[0]: res.data().get("id")} for res in response
            # ]

            # return sorted(response_data, key=lambda i: list(i.keys()))

    def artifacts_created_by_user(self, payload):
        """
        Which nodes were created by user with id of ...
        """
        with self.graph_db.session() as session:
            match_node = match_node_builder()
            query = f"""
                {match_node}-[r]->(n2) 
                where r.user_id={payload.get('user_id')} 
                With *, collect(n)+collect(n2) as nodes 
                Unwind nodes as both_nodes 
                With * 
                RETURN  both_nodes
                """
            response = session.run(query)
            return nodes_edges(response=response)
            # response_data = [
            #     {res.data().get("label")[0]: res.data().get("id")} for res in response
            # ]

            # return sorted(response_data, key=lambda i: list(i.keys()))

    def concept(self, payload):
        """
        Which nodes are associated with a concept ...
        """
        with self.graph_db.session() as session:
            match_node = match_node_builder(node_type="Concept")
            query = f"""
                {match_node}
                -[r:IS_CONCEPT_OF]->(n) 
                Where Cn.concept='{payload.get('curie')}' 
                return n
                """
            response = session.run(query)
            return nodes_edges(response=response)
            # response_data = [
            #     {res.data().get("label")[0]: res.data().get("id")} for res in response
            # ]

            # return sorted(response_data, key=lambda i: list(i.keys()))

    def concept_counts(self, payload):
        """
        Counts of which nodes are associated with a concept
        """
        with self.graph_db.session() as session:
            match_node = match_node_builder(node_type="Concept")
            query = f"""
                {match_node} 
                -[r:IS_CONCEPT_OF]->(n) 
                Where Cn.concept='{payload.get('curie')}' 
                return labels(n) as label, n.id as id 
                """
            response = session.run(query)
            response_data = [
                {res.data().get("label")[0]: res.data().get("id")} for res in response
            ]

            counts = defaultdict(int)
            for response in response_data:
                for key in response:
                    counts[key] += 1
        return counts

    def models_from_code(self, payload):
        """
        Identifies the code source artifact from which a model was extracted
        """
        if payload.get("root_type") not in ("Model"):
            raise HTTPException(
                status_code=400,
                detail="Code artifacts used for model extraction can only be found by providing a Model",
            )
        with self.graph_db.session() as session:
            model_id = payload["root_id"]

            query = """
            MATCH (a:Artifact)<-[r:EXTRACTED_FROM]-(m:Model {id: $model_id})
            RETURN a
            """

            response = session.run(query, {"model_id": model_id})
            response_data = [res.data()["a"]["id"] for res in response]
        return response_data
