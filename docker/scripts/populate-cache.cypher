LOAD CSV WITH HEADERS FROM 'file:///provenance.csv' AS row
// TODO: Include possibility of concepts
CALL apoc.merge.node([row.left_type],{id: row.left}) yield node as l
CALL apoc.merge.node([row.right_type],{id: row.right}) yield node as r
// TODO: Include user_id
CALL apoc.merge.relationship(l,row.relation_type, {},{}, r) yield rel as relation
return relation, l, r;