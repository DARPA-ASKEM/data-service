LOAD CSV WITH HEADERS FROM 'file:///provenance.csv' AS row
// TODO: Include possibility of concepts
CALL apoc.merge.node([row.left_type],{id: toInteger(row.left)}) yield node as l
CALL apoc.merge.node([row.right_type],{id: toInteger(row.right)}) yield node as r
// TODO: Include user_id
with *, COALESCE(row.user_id,1) as userid
CALL apoc.merge.relationship(l,row.relation_type, {user_id: toInteger(userid)},{}, r) yield rel as relation
return relation, l, r;