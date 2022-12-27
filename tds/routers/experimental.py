"""
Experimental provenance search
"""

import enum
import re
from logging import Logger

import openai
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.db import ProvenanceHandler, request_graph_db, request_rdb
from tds.schema.provenance import Provenance
from tds.settings import settings

logger = Logger(__name__)
router = APIRouter()

# MOCKUP DO NOT USE IN PROD: NOT DERIVED FROM ASKEM.DBML
class ProvenanceType(enum.Enum):
    Dataset = "Dataset"
    Model = "Model"
    Plan = "Plan"
    ModelRevision = "ModelRevision"
    Intermediate = "Intermediate"
    Publication = "Publication"
    Run = "Run"


# MOCKUP DO NOT USE IN PROD: NOT DERIVED FROM ASKEM.DBML
class RelationType(enum.Enum):
    DERIVED_FROM = "DERIVED_FROM"
    COPIED_FROM = "COPIED_FROM"
    CITES = "CITES"
    COMBINED_FROM = "COMBINED_FROM"
    EDITED_FROM = "EDITED_FROM"
    USES = "USES"
    EQUIVALENT_OF = "EQUIVALENT_OF"
    EXTRACTED_FROM = "EXTRACTED_FROM"
    REINTERPRETS = "REINTERPRETS"
    GENERATED_BY = "GENERATED_BY"
    BEGINS_AT = "BEGINS_AT"
    DECOMPOSED_FROM = "DECOMPOSED_FROM"
    GLUED_FROM = "GLUED_FROM"
    STRATIFIED_FROM = "STRATIFIED_FROM"


valid_relations = {
    RelationType.COPIED_FROM: [
        (ProvenanceType.ModelRevision, ProvenanceType.ModelRevision)
    ],
    RelationType.CITES: [(ProvenanceType.Publication, ProvenanceType.Publication)],
    RelationType.COMBINED_FROM: [
        (ProvenanceType.ModelRevision, ProvenanceType.ModelRevision)
    ],
    RelationType.EDITED_FROM: [
        (ProvenanceType.ModelRevision, ProvenanceType.ModelRevision)
    ],
    RelationType.USES: [(ProvenanceType.Plan, ProvenanceType.ModelRevision)],
    RelationType.EXTRACTED_FROM: [
        (ProvenanceType.Intermediate, ProvenanceType.Publication),
        (ProvenanceType.Dataset, ProvenanceType.Publication),
        (ProvenanceType.Dataset, ProvenanceType.Run),
    ],
    RelationType.REINTERPRETS: [
        (ProvenanceType.Dataset, ProvenanceType.Run),
        (ProvenanceType.Intermediate, ProvenanceType.Intermediate),
        (ProvenanceType.Intermediate, ProvenanceType.Intermediate),
        (ProvenanceType.Model, ProvenanceType.Intermediate),
    ],
    RelationType.GENERATED_BY: [(ProvenanceType.Dataset, ProvenanceType.ModelRevision)],
    RelationType.BEGINS_AT: [(ProvenanceType.ModelRevision, ProvenanceType.Model)],
    RelationType.DECOMPOSED_FROM: [
        (ProvenanceType.ModelRevision, ProvenanceType.ModelRevision)
    ],
    RelationType.GLUED_FROM: [
        (ProvenanceType.ModelRevision, ProvenanceType.ModelRevision)
    ],
    RelationType.STRATIFIED_FROM: [
        (ProvenanceType.ModelRevision, ProvenanceType.ModelRevision)
    ],
}

db_desc = "Valid relations include:\n"
# NOTE: Should we make these sentences more natural language related?
for relation, mapping in valid_relations.items():
    for (dom, codom) in mapping:
        db_desc += f"{dom}-[relation]->{codom}\n"

preamble = """
I will type "Question:" followed by a question or command in English like "Question: Count all Publications" and you will return a 
single line print "Query:" Followed by an openCypher query like "Query: `match (p:Publication) return count(p)`. 
"""

examples = """
Question: Match all nodes in the database
Query: `Match (n) return n`

Question: Which composed models are derived from Paper with ID of 1?
Query: `Match (M:Model)-[r *1..]-> (i:Intermediate)- [r2:EXTRACTED_FROM]->(p:Publication) where p.id=1 return m`

Question: Which datasets are associated with which model primitives?
Query: `match (d:Dataset)-[r *1..]-(i:Intermediate) return d,r,i`

Question: Return simulators that rely on Primitive with ID of 12 or 4
Query: `match (p:Plan)-[r *1..]->(i:Intermediate) where i.id=4 or i.id=12 return p,r,i`

Question: Which simulators were created by User with ID 999?
Query: `match (p:Plan)-[r:USES]->(mr:ModelRevision) where r.user_id=999 return p`

Question: What are prior versions of this composed model with id 5?
Query: `Match (rev:ModelRevision)<-[r:BEGINS_AT]-(m:Model) where (m.id=5) match (rev2:ModelRevision)<-[r2 *1.. ]-(rev) return rev,rev2`
"""


@router.get("/cql")
def convert_to_cypher(
    query: str,
) -> str:
    """
    Convert English to Cypher.
    """
    user_query = f"Question: {query}\nQuery: "
    prompt = preamble + db_desc + "\n" + examples + "\n" + user_query
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=64,
        api_key=settings.OPENAI_KEY,
    )
    response = completion.choices[0].text
    matched_expression = re.compile(r"`([^`]*)`").fullmatch(response.strip())
    if matched_expression is None:
        raise Exception("OpenAI did not generate a valid response")
    cypher: str = matched_expression.groups(1)[0]
    logger.info("converted '%s' TO `%s`", query, cypher)
    return cypher


@router.get("/provenance")
def search_provenance(
    query: str,
    rdb: Engine = Depends(request_rdb),
    graph_db=Depends(request_graph_db),
) -> str:
    """
    Convert English to Cypher.
    """
    cypher = convert_to_cypher(query)
    raise NotImplemented
