"""
Experimental provenance search
"""

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

preamble = """
I will type "Question:" followed by a question or command in English like "Question: Count all Publications" and you will return a 
single line print "Query:" Followed by an openCypher query like "Query: `match (p:Publication) return count(p)`. Valid labels include
Plan, Run, Intermediate, Model, ModelRevision, Publication.
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
    prompt = preamble + "\n" + examples + "\n" + user_query
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
